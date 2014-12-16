#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import datetime
from pyramid.view import view_config, forbidden_view_config
from pyramid.response import Response
from ..model import atividade
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from wscacicneo.utils.utils import Utils
from wscacicneo.model.user import User
from pyramid.security import (
    remember,
    forget,
)
from pyramid.session import check_csrf_token


class Security(object):
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

    # Autenticação
    #@view_config(route_name='login', renderer='../templates/login.pt')
    #@forbidden_view_config(renderer='../templates/login.pt')
    def login(self):
        """
        Login do sistema
        """
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        result_count = search.result_count
        if(result_count == 0):
            return HTTPFound(location=self.request.route_url('init_config_user'))
        elif(self.usuario_autenticado):
            return HTTPFound(location=self.request.route_url('home'))
        else:
            login_url = self.request.route_url('login')
            referrer = self.request.url
            message = 'Você não tem permissão para isso. Autentique-se.'
            if referrer == login_url:
                referrer = self.request.route_url('root') + 'home' # never use the login form itself as came_from
                message = ''
            came_from = self.request.params.get('came_from', referrer)
            email = ''
            senha = ''
            is_visible = 'none'

            if 'form.submitted' in self.request.params:
                # Valida CSRF do formulário de login
                check_csrf_token(self.request)

                email = self.request.params['email']
                senha = self.request.params['senha']
                senha_hash = Utils.hash_password(senha)
                try:
                    usuario = user_obj.search_user_by_email(email)
                    if usuario.results[0].senha == senha_hash:
                        at = atividade.Atividade(
                            tipo='atividade',
                            usuario=usuario.results[0].nome,
                            descricao='Entrou no sistema',
                            data=datetime.datetime.now()
                        )
                        at.create_atividade()
                        response = Response()
                        id_user = usuario.results[0]._metadata.id_doc
                        headers = remember(
                            self.request,
                            email
                        )

                        # Cria sessão para o usuário
                        session = self.request.session
                        #print(dir(session))
                        session['userid'] = id_user
                        #session.save()

                        # Retorna resposta
                        response = HTTPFound(
                            location=came_from,
                            headers=headers
                        )
                        return response
                    message = 'E-mail ou senha incorretos'
                except:
                    message = 'E-mail ou senha incorretos'

            if message != '':
                is_visible = "block"
            return dict(
                message = message,
                url=self.request.application_url + '/login',
                came_from=came_from,
                email=email,
                senha=senha,
                is_visible=is_visible,
                usuario_autenticado=self.usuario_autenticado,
                )

    #@view_config(route_name='logout', permission="user")
    def logout(self):
        #headers = forget(self.request)

        # Remove sessão do usuário
        session = self.request.session
        session.invalidate()

        #response = Response()
        #response = HTTPFound(location=self.request.route_url('login'),
        #                 headers=headers)
        response = HTTPFound(location=self.request.route_url('login'))
        session.flash('Você se desconectou', queue="error")
        return response
