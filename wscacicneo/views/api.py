#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import requests
import json
import logging
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from .. import config
from .. import search
from ..model import coleta_manual, base_bk

log = logging.getLogger()


class Api(object):
    """
    Views de notificação
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request

    #@view_config(route_name='orgao_config')
    def orgao_config(self):
        """
        Rota que redireciona para o LightBase
        :param request:
        :return:
        """
        response = Response(content_type='text/json')
        try:
            orgao = self.check_permission()
        except HTTPForbidden:
            response.status = 403
            response.text = json.dumps({
                'error_msg': 'Chave inválida ou não encontrada'
            })
            return response
        except HTTPNotFound:
            response.status = 404
            response.text = json.dumps({
                'error_msg': 'Órgão não encontrado. Contate o administrador do sistema para cadastro'
            })
            return response

        # Cria objeto de resposta
        response.status = 200
        response.text = json.dumps({
            'url': orgao.url,
            'coleta': orgao.coleta,
            'habilitar_bot': orgao.habilitar_bot
        })

        return response

    #@view_config(route_name='orgao_coleta')
    def orgao_coleta(self):
        """
        Rota que redireciona para o LightBase
        :param request:
        :return:
        """
        orgao = self.request.matchdict['orgao']
        # Traz dados do órgão
        url = config.REST_URL + '/' + orgao + "/doc"
        resp = requests.get(url)

        # Cria objeto de resposta
        response = Response(content_type='text/json')
        response.status = resp.status_code
        response.text = json.dumps(resp.text)

        return response

    #@view_config(route_name='orgao_relatorio')
    def orgao_relatorio(self):
        """
        Rota que redireciona para o LightBase
        :param request:
        :return:
        """
        orgao = self.request.matchdict['orgao']
        # Traz dados do órgão
        url = config.REST_URL + orgao + "_bk/doc"
        resp = requests.get(url)

        # Cria objeto de resposta
        response = Response(content_type='text/json')
        response.status = resp.status_code
        response.text = resp.text

        return response

    def orgao_create(self):
        """
        Cria base do órgão caso não exista
        :return: Mensagem dizendo se o órgão foi criado
        """
        try:
            orgao = self.check_permission()
        except HTTPForbidden:
            response = Response(content_type='text/json')
            response.status = 403
            response.text = json.dumps({
                'error_msg': 'Chave inválida ou não encontrada'
            })

        orgao = self.request.matchdict['orgao']

        # Faz a requisição para criar o órgão e retorna o Status
        coletaManualBase = coleta_manual.ColetaManualBase(orgao)
        lbbase = coletaManualBase.lbbase

        # Agora cria a nova base
        response = Response(content_type='text/json')
        if coletaManualBase.is_created():
            response.status = 200
            response.text = coletaManualBase.lbbase.json
        else:
            retorno = coletaManualBase.create_base()
            response.status = 200
            response.text = retorno.json

        return response

    def orgao_upload(self):
        try:
            orgao = self.check_permission()
        except HTTPForbidden:
            response = Response(content_type='text/json')
            response.status = 403
            response.text = json.dumps({
                'error_msg': 'Chave inválida ou não encontrada'
            })

        orgao = self.request.matchdict['orgao']
        # Traz dados do órgão
        url = config.REST_URL + orgao + "_bk/doc"

    def check_permission(self):
        """
        Verifica permissão do órgão com base na chave de API
        :return:
        """
        orgao = self.request.matchdict['orgao']
        search_obj = search.orgao.SearchOrgao(
            param=orgao
        )
        orgao_obj = search_obj.search_by_name()
        if orgao_obj is None:
            raise HTTPNotFound

        vars_dict = self.request.GET
        print(vars_dict)
        if vars_dict.get('api_key') is None:
            raise HTTPForbidden

        if orgao_obj.api_key != vars_dict.get('api_key'):
            raise HTTPForbidden

        return orgao_obj