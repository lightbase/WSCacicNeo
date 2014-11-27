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
from wscacicneo.model import descriptions
from wscacicneo.model.reports import Reports
from wscacicneo.search.orgao import SearchOrgao
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import NullDocument
from random import randint

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

    #@view_config(route_name='conf_report', renderer='../templates/conf_report.pt')
    def conf_report(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)

        return {'orgao_doc': result,
                'usuario_autenticado':usuario_autenticado
                }

    #@view_config(route_name='report_itens', renderer='../templates/report.pt', permission="user")
    def report_itens(self):
        orgao_nm = self.request.matchdict['nm_orgao']
        attr = self.request.matchdict['attr']
        child = self.request.matchdict['child']
        nm_orgao = Utils.format_name(orgao_nm)
        report_base = base_reports.ReportsBase(nm_orgao)
        reports_config = config_reports.ConfReports(nm_orgao)
        if(report_base.is_created() == False):
            create_base = report_base.create_base()

            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()

            insert_reports = Utils().create_report(nm_orgao)
            print(insert_reports)
            data = Reports(nm_orgao).count_attribute(attr, child)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {'data': data,
                    'usuario_autenticado':usuario_autenticado,
                    'report_name': attr
                    }
        else:
            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()
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
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {
                    'data': data,
                    'usuario_autenticado':usuario_autenticado,
                    'report_name': attr
                    }

    def put_reports(self):
        data = self.request.params
        item = data['item']
        attr = data['attr']
        nm_orgao = data['nm_base']
        value = data['value']
        data_dic = {attr : {attr+'_item': item, attr+'_amount': value}}
        valor = attr+'_item'
        reports_config = config_reports.ConfReports(nm_orgao)
        search = reports_config.search_item(attr, valor, item)
        print(search)
        data_id = search.results[0]._metadata.id_doc
        document = json.dumps(data_dic)
        put_doc = reports_config.update_coleta(data_id, document)
        return Response(put_doc)

    def report_software(self):
        """
        Rota para os relatórios de software
        """
        orgao_nm = self.request.matchdict['nm_orgao']
        attr = 'softwarelist'
        child = None
        nm_orgao = Utils.format_name(orgao_nm)
        report_base = base_reports.ReportsBase(nm_orgao)
        reports_config = config_reports.ConfReports(nm_orgao)
        if report_base.is_created():
            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()
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
            usuario_autenticado = Utils.retorna_usuario_autenticado(
                email=self.request.authenticated_userid
            )
            return {
                'data': data,
                'usuario_autenticado': usuario_autenticado,
                'report_name': 'software'
            }
        else:
            create_base = report_base.create_base()

            # Carrega base de descrições de campos
            desc_base = descriptions.DescriptionsBase()
            if not desc_base.is_created():
                desc_base.create_base()
            desc_base.load_static()

            insert_reports = Utils().create_report(nm_orgao)
            data = Reports(nm_orgao).count_attribute(attr, child)
            usuario_autenticado = Utils.retorna_usuario_autenticado(
                email=self.request.authenticated_userid
            )
            return {
                'data': data,
                'usuario_autenticado':usuario_autenticado,
                'report_name': 'software'
            }
