#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import json
import datetime
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, forbidden_view_config
from wscacicneo.model import blacklist as blacklist
from wscacicneo.utils.utils import Utils
from liblightbase.lbutils import conv
from .. import config
from .. import search
import uuid
from pyramid.session import check_csrf_token

class Blacklist(object):
    """
    Views de notificação
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    def list_blacklist_items(self):
        blacklist_obj = blacklist.Blacklist(item="name")
        search = blacklist_obj.search_list_items()
        return {'blacklist_doc': search.results,
                'usuario_autenticado': self.usuario_autenticado
                }
