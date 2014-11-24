#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from pyramid.response import Response
from wscacicneo.utils.utils import Utils
from wscacicneo.model.notify import Notify
from pyramid.httpexceptions import HTTPFound
from wscacicneo.search.orgao import SearchOrgao

class Notifications(object):
    """
    Views de notificação
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request

    # Lista de Notificação
    ##@view_config(route_name='list_notify', renderer='../templates/list_notify.pt', permission="gest")
    def list_notify(self):
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        reg = notify_obj.search_list_notify()
        doc = reg.results
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {
            'doc': doc,
            'usuario_autenticado':usuario_autenticado
        }

    def count_notify(self):
        return Response('efdfdfdfdfdfdfdfdlklkkklklklklk')

    #@view_config(route_name='delete_notify', permission="gest")
    def delete_notify(self):
        orgao = self.request.matchdict['orgao']
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        reg = notify_obj.search_notify(orgao)
        doc = reg.results[0]._metadata.id_doc
        delete = notify_obj.delete_notify(doc)
        return HTTPFound(location = self.request.route_url('list_notify'))

    #@view_config(route_name='edit_notify', permission="gest")
    def edit_notify(self):
        orgao = self.request.matchdict['orgao']
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        reg = notify_obj.search_notify(orgao)
        id = reg.results[0]._metadata.id_doc
        document = {
            'orgao' : reg.results[0].orgao,
            'data_coleta' : reg.results[0].data_coleta,
            'notify' : reg.results[0].notify,
            'coment' : reg.results[0].coment,
            'status' : 'Vizualizado'
        }
        doc = json.dumps(document)
        edit = notify_obj.edit_notify(id, doc)
        return HTTPFound(location = self.request.route_url('list_notify'))


    #@view_config(route_name='notify', renderer='../templates/notify_coleta.pt', permission="gest")
    def notify(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)

        return {'orgao_doc': result,
                'usuario_autenticado':usuario_autenticado
                }

    #@view_config(route_name='post_notify', permission="gest")
    def post_notify(self):
        requests = self.request.params
        notify_obj = Notify(
            orgao = requests['orgao'],
            data_coleta = requests['data_coleta'],
            notify = requests['notify'],
            coment = requests['coment'],
            status = requests['status']
        )
        results = notify_obj.create_notify()
        return Response(str(results))
