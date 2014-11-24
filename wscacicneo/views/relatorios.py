#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import re
import logging
from pyramid.view import view_config
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
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
            insert_reports = Utils().create_report(nm_orgao)
            print(insert_reports)
            data = Reports(nm_orgao).count_attribute(attr, child)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {'data': data,
                    'usuario_autenticado':usuario_autenticado
                    }
        else:
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
                    'usuario_autenticado':usuario_autenticado
                    }

    # @view_config(route_name='report_home', permission="user")
    # def report_home(self):
    #     bases = requests.get("http://127.0.0.1/lbgenerator/")
