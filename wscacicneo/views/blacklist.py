#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import json
import datetime
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, forbidden_view_config
from wscacicneo.model import blacklist
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

    def delete_blacklist_item(self):
        session = self.request.session
        blacklist_obj = blacklist.Blacklist(item="name")
        item_name = self.request.matchdict['item']
        search = blacklist_obj.search_item(item_name)
        id = search.results[0]._metadata.id_doc
        delete_item = blacklist_obj.delete_item(id)
        if delete_item:
            session.flash('Sucesso ao excluir o item '+item_name+' da lista de remoção', queue="success")
        else:
            session.flash('Ocorreu um erro ao excluir o item'+item_name+' de lista de remoção', queue="error")
        return HTTPFound(location=self.request.route_url('list_blacklist_items'))

    def post_blacklist_item(self):
        """
        Post doc blacklist
        """
        blacklistbase = blacklist.BlacklistBase().lbbase
        data = self.request.params['item']
        blacklist_obj = blacklist.Blacklist(
            item=data
        )
        id_doc = blacklist_obj.create_item()
        session = self.request.session
        session.flash('Item adicionado à lista de remoção com sucesso', queue="success")
        return Response(str(id_doc))