#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from pyramid.view import view_config
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from wscacicneo.model.reports import Reports
from random import randint

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
        orgao_obj = Orgao(
            nome = 'sahuds',
            cargo = 'cargo',
            coleta = '4h',
            sigla = 'MPOG',
            endereco = 'Esplanada bloco C',
            email = 'admin@planemaneto.gov.br',
            telefone = '(61) 2025-4117',
            url = 'http://api.brlight.net/api'
        )
        search = orgao_obj.search_list_orgaos()
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)

        return {'orgao_doc': search.results,
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
            data = Reports(nm_orgao).count_attribute(attr, child)
            for items in data:
                data_json = {attr : { attr+'_item' : items, attr+'_amount': str(data[items])}}
                document = json.dumps(data_json)
                reports_config.create_coleta(document)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {'data': data,
                    'status_base': create_base,
                    'usuario_autenticado':usuario_autenticado
                    }
        else:
            try:
                get_base = reports_config.get_base()
                document = get_base.results[0].attr
                usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
                return {
                        'data': data,
                        'usuario_autenticado':usuario_autenticado
                        }
            except:
                data = Reports(nm_orgao).count_attribute(attr, child)
                for items in data:
                    data_json = {attr : { attr+'_item' : items, attr+'_amount': str(data[items])}}
                    document = json.dumps(data_json)
                    reports_config.create_coleta(document)
                usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
                return {'data': data,
                        'status_base': create_base,
                        'usuario_autenticado':usuario_autenticado
                        }

            orgao_nm = self.request.matchdict['nm_orgao']
            nm_orgao = Utils.format_name(orgao_nm)
            attr = self.request.matchdict['attr']
            child = self.request.matchdict['child']
            data = Reports(nm_orgao).count_attribute(attr, child)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {
                    'data': data,
                    'usuario_autenticado':usuario_autenticado
                    }

    @view_config(route_name='report_home', permission="user")
    def report_home(self):
        bases = requests.get("http://127.0.0.1/lbgenerator/")
        randint(1,bases.result_count)
