#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from pyramid.view import view_config
from pyramid.response import Response
from .. import config
import requests


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
        orgao = self.request.matchdict['orgao']
        # Traz dados do órgão
        url = config.REST_URL + "orgaos/doc"

        # Busca campos da base
        select_json = {
            "select": [
                "url",
                "coleta",
                "habilitar_bot"
            ],
            "literal": "nome='" + orgao + "'"
        }
        params = {
            '$$': select_json
        }

        resp = requests.get(url, params=params)

        # Cria objeto de resposta
        response = Response(content_type='text/json')
        response.status = resp.status_code
        response.text = resp.text

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
        response.text = resp.text

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