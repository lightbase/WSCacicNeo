#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import requests
import json
import logging
import datetime
import uuid
import os
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from .. import config
from .. import search
from ..model import coleta_manual, base_bk, atividade, notify

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
        response = Response(content_type='application/json')
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

        # Verifica se o órgão existe antes
        search_obj = search.orgao.SearchOrgao(
            param=orgao
        )
        orgao_obj = search_obj.search_by_name()
        if orgao_obj is None:
            raise HTTPNotFound

        # Traz dados do órgão
        url = config.REST_URL + '/' + orgao + self.request.matchdict['path']
        resp = requests.get(
            url=url,
            params=self.request.params
        )

        # Cria objeto de resposta
        response = Response(content_type='application/json')
        response.status = resp.status_code
        response.text = json.dumps(resp.json())

        return response

    #@view_config(route_name='orgao_relatorio')
    def orgao_relatorio(self):
        """
        Rota que redireciona para o LightBase
        :param request:
        :return:
        """
        orgao = self.request.matchdict['orgao']

        # Verifica se o órgão existe antes
        search_obj = search.orgao.SearchOrgao(
            param=orgao
        )
        orgao_obj = search_obj.search_by_name()
        if orgao_obj is None:
            raise HTTPNotFound

        # Traz dados do órgão
        url = config.REST_URL + "/" + orgao + "_bk" + self.request.matchdict['path']
        resp = requests.get(
            url=url,
            params=self.request.params
        )

        # Cria objeto de resposta
        response = Response(content_type='application/json')
        response.status = resp.status_code
        response.text = json.dumps(resp.json())

        return response

    def orgao_create(self):
        """
        Cria base do órgão caso não exista
        :return: Mensagem dizendo se o órgão foi criado
        """
        response = Response(content_type='application/json')
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

        nome_base = self.request.matchdict['orgao']

        # Faz a requisição para criar o órgão e retorna o Status
        coletaManualBase = coleta_manual.ColetaManualBase(nome_base)
        lbbase = coletaManualBase.lbbase

        coleta_bk = base_bk.BaseBackup(orgao=nome_base)
        lbbase_bk = coleta_bk.lbbase

        # Agora cria a nova base
        if coletaManualBase.is_created():
            response.status = 200
            response.text = coletaManualBase.lbbase.json

            # Cria a base de histórico se necessário
            if not coleta_bk.is_created():
                coleta_bk.create_base()

        else:
            retorno = coletaManualBase.create_base()
            # Cria a base de histórico se necessário
            if not coleta_bk.is_created():
                coleta_bk.create_base()

            response.status = 200
            response.text = 'Ok'

        return response

    def orgao_upload(self):
        """
        Envia dados da coleta do órgão para o LBBulk
        :return: Resposta da atividade de inserção
        """
        response = Response(content_type='application/json')
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

        nome_base = self.request.matchdict['orgao']

        # 1 - Registra atividade de envio dos dados para o LBBulk
        at = atividade.Atividade(
            tipo='coleta',
            usuario='WSCBot ' + nome_base,
            descricao='Início de coleta para a base ' + nome_base,
            data=datetime.datetime.now()
        )
        at.create_atividade()

        # 2 - Envia os dados recebidos para o LBBulk
        url_bulk = config.BULK_URL + '/zip_upload'

        default_value = self.request.params.get('default_value')
        if default_value is not None:
            params = {
                'default_value': default_value,
                'default_field': 'nome_orgao',
                'source_name': nome_base,
            }
        else:
            params = {
                'source_name': nome_base
            }
        log.debug("Parâmetros da requisição: %s", params)
        result = requests.post(
            url=url_bulk,
            files={
                'file': self.request.params.get('file').file.read()
            },
            data=params
        )

        if result.status_code != 200:
            log.error("Erro no envio da coleta para a base %s na URL %s\n%s", nome_base, url_bulk, response.text)
            nt = notify.Notify(
                orgao=nome_base,
                data_coleta=datetime.datetime.now(),
                notify="error",
                coment="Erro na inserção da coleta!\n" + result.text,
                status="unread"
            )
            response.status_code = result.status_code
            response.text = result.text

            return response
        else:
            response.status_code = result.status_code
            response.text = result.text

        # 3 - Registra atividade de envio para o LBBulk realizado
        at = atividade.Atividade(
            tipo='coleta',
            usuario='WSCBot ' + nome_base,
            descricao='Coleta finalizada para a base ' + nome_base,
            data=datetime.datetime.now()
        )
        at.create_atividade()

        return response

    def orgao_remove(self):
        response = Response(content_type='application/json')
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

        # 4 - Apaga base da coleta do órgão se tiver sucesso no histórico
        nome_base = self.request.matchdict['orgao']

        at = atividade.Atividade(
            tipo='coleta',
            usuario='WSCBot ' + nome_base,
            descricao='Início de remoção de histórico para a base ' + nome_base,
            data=datetime.datetime.now()
        )
        at.create_atividade()

        # Faz a requisição para criar o órgão e retorna o Status
        coletaManualBase = coleta_manual.ColetaManualBase(nome_base)
        lbbase = coletaManualBase.lbbase

        # Agora apaga a base
        result = coletaManualBase.remove_base()
        if not result:
            log.error("Erro na remoção da base de  coleta %s", nome_base)
            nt = notify.Notify(
                orgao=nome_base,
                data_coleta=datetime.datetime.now(),
                notify="error",
                coment="Erro na remoção da base de  coleta " + nome_base,
                status="unread"
            )

            response.status_code = 500
            response.text = json.dumps({
                'error_msg': "Erro na remoção da base de histórico para a base " + nome_base
            })

            return response

        # 5 - Apaga base de relatórios de qualquer jeito
        base_relatorios = nome_base + "_bk"
        url = config.REST_URL + "/" + base_relatorios
        result = requests.delete(url)
        if result.status_code != 200:
            # Como essa base não é fundamental, notifica mas não falha
            log.error("Erro na remoção da base de relatórios %s", base_relatorios)
            nt = notify.Notify(
                orgao=nome_base,
                data_coleta=datetime.datetime.now(),
                notify="warning",
                coment="Erro na remoção da base de  coleta \n" + result.text,
                status="unread"
            )

        # 6 - Cria base de coletas do órgão
        result = coletaManualBase.create_base()
        if not result:
            log.error("Erro na criação da base de coleta %s", nome_base)
            nt = notify.Notify(
                orgao=nome_base,
                data_coleta=datetime.datetime.now(),
                notify="error",
                coment="Erro na criação da base de  coleta " + nome_base,
                status="unread"
            )

            response.status_code = 500
            response.text = json.dumps({
                'error_msg': "Erro na criação da base de histórico para a base " + nome_base
            })

            return response

        # Se chegou aqui, tudo o que precisava foi removido
        at = atividade.Atividade(
            tipo='coleta',
            usuario='WSCBot ' + nome_base,
            descricao='Fim de remoção de histórico para a base ' + nome_base,
            data=datetime.datetime.now()
        )
        at.create_atividade()

        response.status_code = 200
        response.text = 'Ok'

        return response

    def check_permission(self):
        """
        Verifica permissão do órgão com base na chave de API
        :return:
        """
        print(self.request.params.get('api_key'))
        orgao = self.request.matchdict['orgao']
        # Se for histórico, verifica permissão para o órgão principal
        log.debug("Nome do órgão: %s", orgao)
        if orgao == 'orgaos_bk':
            orgao = self.request.params.get('source_name')

        log.debug(orgao)
        search_obj = search.orgao.SearchOrgao(
            param=orgao
        )
        orgao_obj = search_obj.search_by_name()
        if orgao_obj is None:
            raise HTTPNotFound

        #vars_dict = self.request.GET
        #print(vars_dict)
        if self.request.params.get('api_key') is None:
            raise HTTPForbidden

        if orgao_obj.api_key != self.request.params.get('api_key'):
            raise HTTPForbidden

        return orgao_obj

    def api_doc(self):
        """
        Rota que redireciona para o LightBase Docs
        :param request: Requisiçao original
        :return: Retorno do LBGenerator
        """
        url = config.REST_URL + "/api-docs" + self.request.matchdict['path']
        resp = requests.get(
            url=url,
            params=self.request.params
        )

        # Cria objeto de resposta
        response = Response(content_type='application/json')
        response.status = resp.status_code
        response.text = json.dumps(resp.json())

        return response
