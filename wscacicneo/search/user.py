#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import requests
import json
import ast
from liblightbase.lbsearch.search import *
from liblightbase.lbutils import conv
from ..model import user
from .. import config

user_base = user.UserBase()
log = logging.getLogger()


class SearchUser(object):
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
        self.orgao_base = user_base

    def search_by_name(self):
        search = Search(
            select=[
                "*"
            ],
            literal="document->>'matricula' = '" + self.param + "'",
            limit=1
        )
        url = config.REST_URL
        url += "/users/doc"
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
                user_obj = user.User(
                    nome=doc.get('nome'),
                    matricula=doc.get('matricula'),
                    email=doc.get('email'),
                    orgao=doc.get('orgao'),
                    telefone=doc.get('telefone'),
                    cargo=doc.get('cargo'),
                    setor=doc.get('setor'),
                    permissao=doc.get('permissao'),
                    senha=doc.get('senha'),
                    itens=doc.get('itens'),
                    favoritos=doc.get('favoritos')
                )
                return user_obj
            return response.json()
        else:
            log.error("Erro na busca pelo usuario %s\n%s", self.param, response.text)
            return None

    def list_by_name(self):
        orderby = OrderBy(asc=['email'])
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
            search.literal = "document->>'email' = '" + self.param + "'",
        url = config.REST_URL
        url += "/users/doc"
        vars = {
            '$$': search._asjson()
        }

        response = requests.get(url, params=vars)
        log.debug(response.url)
        r_json = response.json()
        print(r_json)

        saida = list()
        for i in range(0, r_json['result_count']):
            try:
                result = r_json['results'][i]
            except IndexError:
                break

            if self.return_object:
                #print(response.json())
                doc = result
                user_obj = user.User(
                    nome=doc.get('nome'),
                    matricula=doc.get('matricula'),
                    email=doc.get('email'),
                    orgao=doc.get('orgao'),
                    telefone=doc.get('telefone'),
                    cargo=doc.get('cargo'),
                    setor=doc.get('setor'),
                    permissao=doc.get('permissao'),
                    senha=doc.get('senha'),
                )

                saida.append(user_obj)
            else:
                saida.append(result)

        return saida
