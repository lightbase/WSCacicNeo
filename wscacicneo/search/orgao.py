#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import requests
import json
import ast
from liblightbase.lbsearch.search import *
from liblightbase.lbutils import conv
from ..model import orgao
from .. import config

orgao_base = orgao.OrgaoBase()
log = logging.getLogger()


class SearchOrgao(object):
    """
    Classe de métodos para busca do órgão
    """

    def __init__(self, param=None, return_object=True):
        """
        Método construtor
        :param param: Parâmetro de busca
        :param return_object: Se verdadeiro retorna o objeto. Caso contrário retorna JSON
        """
        self.param = param
        self.return_object = return_object
        self.orgao_base = orgao_base

    def search_by_name(self):
        search = Search(
            select=[
                "*"
            ],
            literal="document->>'sigla' = '" + self.param + "'",
            limit=1
        )
        url = config.REST_URL
        url += "/orgaos/doc"
        vars = {
            '$$': search._asjson()
        }

        response = requests.get(url, params=vars)
        log.debug(response.url)
        r_json = response.json()

        if r_json['result_count'] > 0:
            # Verifica se deve retornar objeto
            if self.return_object:
                #print(response.json())
                doc = r_json['results'][0]
                orgao_obj = orgao.Orgao(
                    nome=doc.get('nome'),
                    pretty_name=doc.get('pretty_name'),
                    siorg=doc.get('siorg'),
                    gestor=doc.get('gestor'),
                    cargo=doc.get('cargo'),
                    coleta=doc.get('coleta'),
                    sigla=doc.get('sigla'),
                    endereco=doc.get('endereco'),
                    email=doc.get('email'),
                    telefone=doc.get('telefone'),
                    url=doc.get('url'),
                    habilitar_bot=doc.get('habilitar_bot'),
                    api_key=doc.get('api_key')
                )
                return orgao_obj
            return response.json()
        else:
            log.error("Erro na busca pelo orgao %s\n%s", self.param, response.text)
            return None

    def list_by_name(self):
        orderby = OrderBy(asc=['nome'])
        search = Search(
            select=[
                "*"
            ],
            #literal="document->>'nome' = '" + self.param + "'",
            limit=None,
            offset=0,
            order_by=orderby
        )
        if self.param is not None:
            search.literal = "document->>'sigla' = '" + self.param + "'",
        url = config.REST_URL
        url += "/orgaos/doc"
        vars = {
            '$$': search._asjson()
        }

        response = requests.get(url, params=vars)
        log.debug(response.url)
        r_json = response.json()
        #print(r_json)

        saida = list()
        for i in range(0, r_json['result_count']):
            try:
                result = r_json['results'][i]
            except IndexError:
                break

            if self.return_object:
                #print(response.json())
                doc = result
                orgao_obj = orgao.Orgao(
                    nome=doc.get('nome'),
                    pretty_name=doc.get('pretty_name'),
                    gestor=doc.get('gestor'),
                    cargo=doc.get('cargo'),
                    coleta=doc.get('coleta'),
                    sigla=doc.get('sigla'),
                    endereco=doc.get('endereco'),
                    email=doc.get('email'),
                    telefone=doc.get('telefone'),
                    url=doc.get('url'),
                    habilitar_bot=doc.get('habilitar_bot'),
                    api_key=doc.get('api_key')
                )
                saida.append(orgao_obj)
            else:
                saida.append(result)

        return saida
