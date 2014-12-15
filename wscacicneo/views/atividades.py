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


    def list_atividades(self):
        """
        Lista as ultimas 100 atividades
        """
        limit_docs = 100
        atividade_obj = Utils.create_atividade_obj()
        results = atividade_obj.search_list_atividades(limit_docs)
        usuario_autenticado = Utils.retorna_usuario_autenticado(user_id=self.request.session['userid'])

        return {'data': results.results,
                'usuario_autenticado': usuario_autenticado,
               }

    def list_atividades_bot(self):
        """
        Lista as ultimas 100 atividades
        """
        limit_docs = 100
        atividade_obj = Utils.create_atividade_obj()
        results = atividade_obj.search_list_bot()
        usuario_autenticado = Utils.retorna_usuario_autenticado(user_id=self.request.session['userid'])

        return {'data': results.results,
                'usuario_autenticado': usuario_autenticado,
               }

