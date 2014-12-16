#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from wscacicneo.utils.utils import Utils
from wscacicneo.model import coleta_manual
from pyramid.response import Response
from pyramid.view import view_config
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.reports import Reports
from wscacicneo.search.orgao import SearchOrgao


class Coleta(object):
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

    # Reports
    #@view_config(route_name='create_orgao', permission="gest")permission="gest"
    def create_orgao(self):
        nm_orgao = Utils.format_name(self.request.matchdict['nm_orgao'])
        coletaManualBase = coleta_manual.ColetaManualBase(nm_orgao)
        lbbase = coletaManualBase.lbbase
        retorno = coletaManualBase.create_base()
        return Response(retorno.json)

    # Coleta
    #@view_config(route_name='cadastro_coleta', renderer='templates/cadastro_coleta.pt', permission="gest")
    def cadastro_coleta(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()

        return {'orgao_doc': result,
                'usuario_autenticado': self.usuario_autenticado
                }


    #@view_config(route_name='post_coleta_manual', permission="gest")
    def post_coleta_manual(self):
        """
        Post doc ColetaManual
        """
        document = json.loads(self.request.params['documento'])
        nm_base = document['orgao']
        data_coleta = document['data_coleta']
        softwarelist = document['softwarelist']
        win32_processor_manufacturer = document['win32_processor_manufacturer']
        win32_processor_numberoflogicalprocessors = document['win32_processor_numberoflogicalprocessors']
        win32_processor_caption = document['win32_processor_caption']
        operatingsystem_version = document['operatingsystem_version']
        operatingsystem_installdate = document['operatingsystem_installdate']
        operatingsystem_caption = document['operatingsystem_caption']
        win32_bios_manufacturer = document['win32_bios_manufacturer']

        nm_base_formatted = Utils.format_name(nm_base)
        coleta_dict= {
            "data_coleta": data_coleta,
            "win32_processor": {
                "win32_processor_manufacturer": win32_processor_manufacturer,
                "win32_processor_numberoflogicalprocessors": win32_processor_numberoflogicalprocessors,
                "win32_processor_caption": win32_processor_caption
            },
            "operatingsystem": {
                "operatingsystem_version": operatingsystem_version,
                "operatingsystem_installdate": operatingsystem_installdate,
                "operatingsystem_caption": operatingsystem_caption
            },
            "softwarelist":softwarelist,
            "win32_bios": {
                "win32_bios_manufacturer": win32_bios_manufacturer
            }
        }
        dumps = json.dumps(coleta_dict)
        id_doc = Reports(nm_base_formatted,response_object=False).create_coleta(dumps)
        session = self.request.session
        session.flash('Cadastro realizado com sucesso', queue="success")
        return Response(str(id_doc))

