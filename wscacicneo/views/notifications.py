#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from pyramid.response import Response
from wscacicneo.utils.utils import Utils
from wscacicneo.model.notify import Notify
from pyramid.httpexceptions import HTTPFound
from wscacicneo.search.orgao import SearchOrgao
from wscacicneo.utils.utils import Utils
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.user import User


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
        type_map = {
            '1': 'Erro na Coleta',
            '2': 'Coleta Desatualizada',
            '3': 'Outros'}
        if self.request.params.get('type'):
            notify_type = type_map[self.request.params['type']]
        else:
            notify_type = None
        usuario_autenticado = Utils.retorna_usuario_autenticado(
            user_id=self.request.session['userid'])
        reg = notify_obj.search_list_notify(notify_type,
            usuario_autenticado)
        doc = reg.results
        return {
            'doc': doc,
            'usuario_autenticado':usuario_autenticado
        }

    def count_notify(self):
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        user = Utils.retorna_usuario_autenticado(
            user_id=self.request.session['userid'])
        response = {
            'type-1': notify_obj.get_count(user, 'Erro na Coleta'),
            'type-2': notify_obj.get_count(user, 'Coleta Desatualizada'),
            'type-3': notify_obj.get_count(user, 'Outros')}
        response = json.dumps(response)
        return Response(response)

    #@view_config(route_name='delete_notify', permission="gest")
    def delete_notify(self):
        id = self.request.matchdict['orgao']
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        delete = notify_obj.delete_notify(id)
        session = self.request.session
        if delete:
            session.flash('Cadastro realizado com sucesso', queue="success")
        else:
            session.flash('Erro ao apagar a notificação', queue="error")
        return HTTPFound(location = self.request.route_url('list_notify'))

    #@view_config(route_name='edit_notify', permission="gest")
    def edit_notify(self):
        id = self.request.matchdict['orgao']
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        edit = notify_obj.edit_notify_attr(id, ['status'], 'Visualizado')
        return HTTPFound(location = self.request.route_url('list_notify'))


    #@view_config(route_name='notify', renderer='../templates/notify_coleta.pt', permission="gest")
    def notify(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()
        usuario_autenticado = Utils.retorna_usuario_autenticado(user_id=self.request.session['userid'])

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
        session = self.request.session
        session.flash('Cadastro realizado com sucesso', queue="success")
        return Response(str(results))

    def notify_orgaos_users(self):
        """
        Retorna o numero de órgãos e usuarios do sistema
        """
        orgao_obj = Utils.create_orgao_obj()
        user_obj = Utils.create_user_obj()
        result_user = user_obj.search_list_users()
        result_orgao = orgao_obj.search_list_orgaos()
        data = {
            'count_orgao' : result_orgao.result_count,
            'count_user' : result_user.result_count
            }
        results = json.dumps(data)
        return Response(results)

