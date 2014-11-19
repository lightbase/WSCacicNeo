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

    @view_config(route_name='listorgao', renderer='../templates/list_orgao.pt', permission="admin")
    def listorgao(self):
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

    @view_config(route_name='config_orgao', renderer='../templates/config_orgao.pt', permission="admin")
    def config_orgao(self):
        sigla = self.request.matchdict['sigla']
        orgao_obj = Orgao(
            nome = 'asdsad',
            cargo = 'cargo',
            coleta = '4h',
            sigla = sigla,
            endereco = 'Esplanada bloco C',
            email = 'admin@planemaneto.gov.br',
            telefone = '(61) 2025-4117',
            url = 'http://api.brlight.net/api'
        )
        search = orgao_obj.search_orgao(sigla)
        usuario_autenticado = Utils.retorna_usuario_autenticado(self.request.authenticated_userid)

        return {
            'nome' : search.results[0].nome,
            'cargo' : search.results[0].cargo,
            'sigla' : search.results[0].sigla,
            'endereco' : search.results[0].endereco,
            'email' : search.results[0].email,
            'telefone' : search.results[0].telefone,
            'usuario_autenticado':usuario_autenticado
        }

    @view_config(route_name='editorgao', renderer='../templates/editarorgao.pt', permission="admin")
    def editorgao(self):
        sigla = self.request.matchdict['sigla']
        orgao_obj = Orgao(
            nome = 'asdsad',
            cargo = 'cargo',
            coleta = '4h',
            sigla = sigla,
            endereco = 'Esplanada bloco C',
            email = 'admin@planemaneto.gov.br',
            telefone = '(61) 2025-4117',
            url = 'http://api.brlight.net/api'
        )
        search = orgao_obj.search_orgao(sigla)
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)

        return {
            'nome' : search.results[0].nome,
            'cargo' : search.results[0].cargo,
            'coleta' : search.results[0].coleta,
            'sigla' : search.results[0].sigla,
            'endereco' : search.results[0].endereco,
            'email' : search.results[0].email,
            'telefone' : search.results[0].telefone,
            'url' : search.results[0].url,
            'usuario_autenticado':usuario_autenticado
        }

    @view_config(route_name='post_orgao', permission="admin")
    def post_orgao(self):
        """
        Post doc órgãos
        """
        rest_url = REST_URL
        orgaobase = model_orgao.OrgaoBase().lbbase
        doc = self.request.params
        orgao_obj = Orgao(
            nome=doc['nome'],
            cargo=doc['gestor'],
            coleta=doc['coleta'],
            sigla=doc['sigla'],
            endereco=doc['end'],
            email=doc['email'],
            telefone=doc['telefone'],
            url=doc.get('url')
        )
        id_doc = orgao_obj.create_orgao()
        return Response(str(id_doc))

    @view_config(route_name='put_orgao', permission="admin")
    def put_orgao(self):
        """
        Edita um doc apartir do id
        """
        params = self.request.params
        sigla = params['id']
        orgao_obj = Orgao(
            nome = params['nome'],
            cargo = params['gestor'],
            coleta = params['coleta'],
            sigla = params['sigla'],
            endereco = params['end'],
            email = params['email'],
            telefone = params['telefone'],
            url = params['url']
        )
        orgao = {
            'nome' : params['nome'],
            'cargo' : params['gestor'],
            'coleta' : params['coleta'],
            'sigla' : params['sigla'],
            'endereco' : params['end'],
            'email' : params['email'],
            'telefone' : params['telefone'],
            'url' : params['url']
        }
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(orgao)
        edit = orgao_obj.edit_orgao(id, doc)
        return Response(edit)

    @view_config(route_name='delete_orgao', permission="admin")
    def delete_orgao(self):
        """
        Deleta doc apartir do id
        """
        doc = self.request.params
        sigla = self.request.matchdict['sigla']
        orgao_obj = Orgao(
            nome = 'asdasd',
            cargo = 'asdasdasd',
            coleta = 'asdasdasd',
            sigla = 'asdasdas',
            endereco = 'asdsad',
            email = 'asdsad',
            telefone = 'sadasd',
            url = 'sadasd'
        )
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        delete = orgao_obj.delete_orgao(id)
        return HTTPFound(location = self.request.route_url('listorgao'))

