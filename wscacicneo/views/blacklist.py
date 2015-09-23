#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import json
import datetime
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, forbidden_view_config
from wscacicneo.model import blacklist
from wscacicneo.utils.utils import Utils
from liblightbase.lbutils import conv
from .. import config
from .. import search
import uuid
from pyramid.session import check_csrf_token
from wscacicneo.search.orgao import SearchOrgao
from wscacicneo.utils.utils import Utils
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from wscacicneo.model import reports
from wscacicneo.model import all_reports
from wscacicneo.model import descriptions
from wscacicneo.model.reports import Reports
from liblightbase.lbsearch.search import NullDocument


class Blacklist(object):
    """
    Views de notificação
    """

    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    def list_blacklist_items(self):
        blacklist_obj = blacklist.Blacklist(item="name")
        search = blacklist_obj.search_list_items()
        results = search.results
        index_itens = dict()
        key_number = 1
        for elm in results:
            index_itens[key_number] = elm.item
            key_number = key_number + 1
        return {'blacklist_doc': index_itens,
                'usuario_autenticado': self.usuario_autenticado
                }

    def delete_blacklist_item(self):
        session = self.request.session
        blacklist_obj = blacklist.Blacklist(item="name")
        item_name = self.request.matchdict['item']
        search = blacklist_obj.search_item(item_name)
        id = search.results[0]._metadata.id_doc
        delete_item = blacklist_obj.delete_item(id)
        if delete_item:
            session.flash('Sucesso ao excluir o item ' + item_name + ' da lista de remoção', queue="success")
        else:
            session.flash('Ocorreu um erro ao excluir o item' + item_name + ' de lista de remoção', queue="error")
        return HTTPFound(location=self.request.route_url('list_blacklist_items'))

    def post_blacklist_item(self):
        """
        Post doc blacklist
        """
        blacklistbase = blacklist.BlacklistBase().lbbase
        data = self.request.params['item']
        blacklist_obj = blacklist.Blacklist(
            item=data
        )
        id_doc = blacklist_obj.create_item()
        session = self.request.session
        session.flash('O Item "' + data + '" foi adicionado à lista de remoção com sucesso', queue="success")
        return Response(str(id_doc))

    def add_blacklist_item(self):
        data = list()
        index_itens = dict()
        data_list = list()
        search = SearchOrgao()
        orgaos = [org.nome for org in search.list_by_name()]

        for orgao in orgaos:
            data = self.report_software_for_blacklist(orgao)
            # Remove valores duplicados
            for item in data:
                if item not in data_list:
                    data_list.append(item)
        index_itens = Utils.dict_items_indexed(data_list)
        return {
            'usuario_autenticado': self.usuario_autenticado,
            'index_itens': index_itens
        }

    def report_software_for_blacklist(self, orgao):
        """
        Rota para os relatórios de software
        """
        view_type = 'detailed'
        orgao_nm = orgao
        nm_orgao = orgao
        pretty_name_orgao = Utils.pretty_name_orgao(orgao_nm)
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
                item = getattr(parent, attr + '_item')
                amount = getattr(parent, attr + '_amount')
                data[item] = amount
            index_itens = dict()
            key_number = 1
            if view_type == 'simple':
                data = Utils.group_data(data)
            for item in data.keys():
                index_itens[key_number] = item
                key_number = key_number + 1
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
        items = list(index_itens.values())
        return items

