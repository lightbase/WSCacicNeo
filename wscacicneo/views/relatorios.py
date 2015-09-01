#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import re
import logging
from pyramid.view import view_config
from pyramid.response import Response
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from wscacicneo.model import reports
from wscacicneo.model import all_reports
from wscacicneo.model import descriptions
from wscacicneo.model.reports import Reports
from wscacicneo.search.orgao import SearchOrgao
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import NullDocument
from random import randint
from pyramid.session import check_csrf_token
from pyramid.httpexceptions import HTTPFound

log = logging.getLogger()


class Relatorios(object):
    """
    Métodos básicos do sistema
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    #@view_config(route_name='conf_report', renderer='../templates/conf_report.pt')
    def conf_report(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()

        return {'orgao_doc': result,
                'usuario_autenticado': self.usuario_autenticado
                }

    #@view_config(route_name='report_itens', renderer='../templates/report.pt', permission="user")
    def report_itens(self):
        orgao_nm = self.request.matchdict['nm_orgao']
        attr = self.request.matchdict['attr']
        child = self.request.matchdict['child']
        nm_orgao = Utils.format_name(orgao_nm)
        report_base = base_reports.ReportsBase(nm_orgao)
        reports_config = config_reports.ConfReports(nm_orgao)
        ###
        reports_count = reports.Reports(nm_orgao).get_base_orgao()
        ###
        count_reports = reports_count.result_count
        if(report_base.is_created() == False):
            create_base = report_base.create_base()

            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()

            insert_reports = Utils().create_report(nm_orgao)
            #print(insert_reports)
            data = Reports(nm_orgao).count_attribute(attr, child)

        else:
            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()
            if attr != 'todos':
                get_base = reports_config.get_attribute(attr)
                results = get_base.results
                data = dict()
                for elm in results:
                    if isinstance(elm, NullDocument):
                        continue
                    parent = getattr(elm, attr)
                    item = getattr(parent, attr+'_item')
                    amount = getattr(parent, attr+'_amount')
                    data[item] = amount

            else:
                data = dict()
                for attri in ['softwarelist','win32_physicalmemory', 'win32_bios', 'win32_diskdrive', 'operatingsystem', 'win32_processor']:
                    data_parcial = dict()
                    get_base = reports_config.get_attribute(attri)
                    results = get_base.results

                    for elm in results:
                        if isinstance(elm, NullDocument):
                            continue
                        parent = getattr(elm, attri)
                        item = getattr(parent, attri+'_item')
                        amount = getattr(parent, attri+'_amount')
                        data_parcial[item] = amount
                    data[attri] = data_parcial

        if attr != 'todos':
            data = Utils.computers_not_found(data, count_reports)
            index_itens = dict()
            key_number = 1
            for item in data.keys():
                index_itens[key_number] = item
                key_number = key_number + 1
        else:
            data = Utils.computers_not_found(data, count_reports)
            index_itens = dict()
            key_number = 1
            for datas in data.keys():
                if isinstance(data[datas], type(dict())):
                    for item in data[datas].keys():
                        index_itens[key_number] = item
                        key_number = key_number + 1
                else:
                    index_itens[key_number] = datas
                    key_number = key_number +1
        return {
            'data': data,
            'index_itens': index_itens,
            'count' : count_reports,
            'usuario_autenticado': self.usuario_autenticado,
            'report_name': attr,
            'orgao_name': orgao_nm,
        }

    def put_reports(self):
        if self.usuario_autenticado:
            data = self.request.params
            if self.usuario_autenticado.permissao == 'Administrador' or (self.usuario_autenticado.permissao == 'Gestor' and self.usuario_autenticado.orgao == data['nm_base']):
                item_key = data['item']
                item = data['dict_itens['+item_key+']']
                attr = data['attr']
                if attr == 'software':
                    attr = 'softwarelist'
                nm_orgao = data['nm_base']
                value = data['value']
                data_dic = {attr : {attr+'_item': item, attr+'_amount': int(value)}}
                valor = attr+'_item'
                reports_config = config_reports.ConfReports(nm_orgao)
                search = reports_config.search_item(attr, valor, item)
                #print(search)
                data_id = search.results[0]._metadata.id_doc
                document = json.dumps(data_dic)
                put_doc = reports_config.update_coleta(data_id, document)
                session = self.request.session
                session.flash('Alteração realizada com sucesso', queue="success")
                return Response(put_doc)
            else:
                session = self.request.session
                session.flash('Você não tem permissão para alterar.', queue="error")
                return Response(None)
        else:
            session = self.request.session
            session.flash('Você não tem permissão para alterar.', queue="error")
            return Response(None)

    def report_software(self):
        """
        Rota para os relatórios de software
        """
        view_type =''
        view_type_pt = self.request.matchdict['view_type']
        if view_type_pt == 'simples':
            view_type = 'simple'
        elif view_type_pt == 'detalhado':
            view_type = 'detailed'
        orgao_nm = self.request.matchdict['nm_orgao']
        nm_orgao = self.request.matchdict['nm_orgao']
        reports_count = reports.Reports(nm_orgao).get_base_orgao()
        count_reports = reports_count.result_count
        attr = 'softwarelist'
        child = None
        nm_orgao = Utils.format_name(orgao_nm)
        # Cria base de relatórios do órgão
        report_base = base_reports.ReportsBase(nm_orgao)

        # Base de configurações do relatório
        reports_config = config_reports.ConfReports(nm_orgao)

        if report_base.is_created():
            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()

            get_base = reports_config.get_attribute(attr)
            results = get_base.results

            # Aqui conta todos os campos
            data = dict()
            for elm in results:
                if isinstance(elm, NullDocument):
                    continue
                parent = getattr(elm, attr)
                item = getattr(parent, attr+'_item')
                amount = getattr(parent, attr+'_amount')
                data[item] = amount
            index_itens = dict()
            key_number = 1
            if view_type == 'simple':
                data = Utils.group_data(data)
            for item in data.keys():
                index_itens[key_number] = item
                key_number = key_number + 1
            return {
                'data': data,
                'index_itens': index_itens,
                'count': count_reports,
                'usuario_autenticado': self.usuario_autenticado,
                'report_name': 'software',
                'view_type': view_type,
                'orgao_name': nm_orgao
            }
        else:
            create_base = report_base.create_base()

            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()
            insert_reports = Utils().create_report(nm_orgao)
            if view_type == 'simple':
                data = Reports(nm_orgao).count_attribute(attr, child, True)
            elif view_type == 'detailed':
                data = Reports(nm_orgao).count_attribute(attr, child)
            return HTTPFound(location=self.request.route_url('report_software', view_type=view_type_pt, nm_orgao=orgao_nm))
            # index_itens = dict()
            # key_number = 1
            # for item in data.keys():
            #     index_itens[key_number] = item
            #     key_number = key_number + 1
            # return {
            #     'data': data,
            #     'index_itens': index_itens,
            #     'count': count_reports,
            #     'usuario_autenticado': self.usuario_autenticado,
            #     'report_name': 'software',
            #     'view_type': view_type


    def post_reports(self):
        """
        Insere dados na base de relatorios
        """
        data = self.request.params
        attr = data['attr']
        if attr == 'software':
            attr = 'softwarelist'
        orgao = data['base']
        item = data['item']
        value = data['value']
        nm_orgao = Utils.format_name(orgao)
        dumps = {attr : {attr+'_item': str(item), attr+'_amount': int(value)}}
        document = json.dumps(dumps)
        reports_config = config_reports.ConfReports(nm_orgao)
        response = reports_config.create_coleta(document)
        session = self.request.session
        session.flash('Cadastro realizado com sucesso', queue="success")
        return Response(str(response))

    def delete_reports(self):
        nm_base = self.request.params['base']
        base = base_reports.ReportsBase(nm_base)
        results = base.remove_base()
        session = self.request.session
        if results:
            session.flash('Atualização do relatório realizada com sucesso', queue="success")
        else:
            session.flash('Erro ao atualizar o relatório', queue="error")
        return Response(str(results))

    def json_csv(self):
        """
        Gerencia o download do csv do relatorio
        """
        data = self.request.params.get('data')
        header = self.request.params.get('header')

        rows = json.loads(data)
        if header is not None:
            header = json.loads(header)

        filename = 'software.csv'
        self.request.response.content_disposition = 'attachment;filename=' + filename

        return {
            'header': header,
            'rows': rows
        }


