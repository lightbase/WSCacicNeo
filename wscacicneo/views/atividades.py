#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import json
from random import randint
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, forbidden_view_config
from wscacicneo.model import user as model_usuario
from wscacicneo.model import orgao as model_orgao
from wscacicneo.model import notify as model_notify
from wscacicneo.model import reports as model_reports
from wscacicneo.model import atividade
from wscacicneo.utils.utils import Utils
from wscacicneo.model import config_reports
from wscacicneo import config
from liblightbase.lbsearch.search import NullDocument
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.session import check_csrf_token

class Atividades(object):
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



    def list_atividades(self):
        """
        Lista as ultimas 100 atividades
        """
        limit_docs = 100
        atividade_obj = Utils.create_atividade_obj()
        results = atividade_obj.search_list_atividades(limit_docs)

        return {'data': results.results,
                'usuario_autenticado': self.usuario_autenticado,
               }

    def list_atividades_bot(self):
        """
        Lista as ultimas 100 atividades
        """
        limit_docs = 100
        atividade_obj = Utils.create_atividade_obj()
        results = atividade_obj.search_list_bot()

        return {'data': results.results,
                'usuario_autenticado': self.usuario_autenticado,
               }

