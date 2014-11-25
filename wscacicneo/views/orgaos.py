#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import json
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, forbidden_view_config
from wscacicneo.model import orgao as model_orgao
from wscacicneo.utils.utils import Utils
from wscacicneo.model.orgao import Orgao
from liblightbase.lbutils import conv
from .. import config
from .. import search
import uuid
import ast


class Orgaos(object):
    """
    Views de notificação
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request

    def listorgao(self):
        orgao_obj = Orgao(
            nome = 'sahuds',
            cargo = 'cargo',
            gestor = 'gestor',
            coleta = '4',
            sigla = 'MPOG',
            endereco = 'Esplanada bloco C',
            email = 'admin@planemaneto.gov.br',
            telefone = '(61) 2025-4117',
            url = 'http://api.brlight.net/api',
            api_key = '12242142141'
        )
        search = orgao_obj.search_list_orgaos()
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {'orgao_doc': search.results,
                'usuario_autenticado':usuario_autenticado
                }

    def config_orgao(self):
        sigla = self.request.matchdict['sigla']

        search_obj = search.orgao.SearchOrgao(
            param=sigla
        )
        orgao_obj = search_obj.search_by_name()
        usuario_autenticado = Utils.retorna_usuario_autenticado(self.request.authenticated_userid)

        saida = orgao_obj.orgao_to_dict()
        # Coloca algum valor na URL
        if saida.get('url') is None:
            saida['url'] = self.request.application_url

        saida['usuario_autenticado'] = usuario_autenticado

        return saida

    def editorgao(self):
        sigla = self.request.matchdict['sigla']
        search_obj = search.orgao.SearchOrgao(
            param=sigla
        )
        orgao_obj = search_obj.search_by_name()
        usuario_autenticado = Utils.retorna_usuario_autenticado(self.request.authenticated_userid)

        saida = orgao_obj.orgao_to_dict()
        if saida.get('url') is None:
            saida['url'] = self.request.application_url
        saida['usuario_autenticado'] = usuario_autenticado

        return saida

    def post_orgao(self):
        """
        Post doc órgãos
        """
        rest_url = config.REST_URL
        orgaobase = model_orgao.OrgaoBase().lbbase
        doc = self.request.params
        orgao_obj = Orgao(
            nome=doc.get('nome'),
            cargo=doc.get('cargo'),
            gestor=doc.get('gestor'),
            coleta=int(doc.get('coleta')),
            sigla=doc.get('sigla'),
            endereco=doc.get('end'),
            email=doc.get('email'),
            telefone=doc.get('telefone'),
            url=doc.get('url'),
            habilitar_bot=ast.literal_eval(doc.get('habilitar_bot')),
            api_key=doc.get('api_key')
        )
        id_doc = orgao_obj.create_orgao()
        return Response(str(id_doc))

    def put_orgao(self):
        """
        Edita um doc apartir do id
        """
        doc = self.request.params
        sigla = doc['id']
        orgao_obj = Orgao(
            nome=doc.get('nome'),
            gestor=doc.get('gestor'),
            cargo=doc.get('cargo'),
            coleta=int(doc.get('coleta')),
            sigla=doc.get('sigla'),
            endereco=doc.get('end'),
            email=doc.get('email'),
            telefone=doc.get('telefone'),
            url=doc.get('url'),
            habilitar_bot=ast.literal_eval(doc.get('habilitar_bot')),
            api_key=doc.get('api_key')
        )
        orgao = orgao_obj.orgao_to_dict()
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(orgao)
        edit = orgao_obj.edit_orgao(id, doc)
        return Response(edit)

    def delete_orgao(self):
        """
        Deleta doc apartir do id
        """
        doc = self.request.params
        sigla = self.request.matchdict['sigla']
        orgao_obj = Orgao(
            nome = 'asdasd',
            gestor= 'gestor',
            cargo = 'asdasdasd',
            coleta = '3',
            sigla = 'asdasdas',
            endereco = 'asdsad',
            email = 'asdsad',
            telefone = 'sadasd',
            url = 'sadasd',
            api_key=doc.get('api_key')
        )
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        delete = orgao_obj.delete_orgao(id)
        return HTTPFound(location = self.request.route_url('listorgao'))

    # Views de Orgão
    def orgao(self):
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {
            'usuario_autenticado': usuario_autenticado,
            'api_key': uuid.uuid4()
        }
