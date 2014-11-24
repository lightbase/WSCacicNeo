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
from wscacicneo.model import atividade as model_atividade
from wscacicneo.utils.utils import Utils
from wscacicneo import config


class Home(object):
    """
    Métodos básicos do sistema
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request

    # Views de configuração
    #@view_config(route_name='blankmaster', renderer='../../templates/blankmaster.pt')
    def blankmaster(self):
        return HTTPFound(location=self.request.route_url("home"))

    #@view_config(route_name='master', renderer='../templates/master.pt')
    def master(self):
        return HTTPFound(location=self.request.route_url("home"))

    #@view_config(route_name='root')
    def root(self):
        return HTTPFound(location=self.request.route_url("home"))

    # Views básicas
    #@view_config(route_name='create_config_initial')
    def create_config_initial(self):
        user_base = model_usuario.UserBase()
        orgao_base = model_orgao.OrgaoBase()
        notify_base = model_notify.NotifyBase()
        atividade_base = model_atividade.AtividadeBase()
        #print(orgao_base.rest_url)
        # Cria tudo que precisa para carregar.
        # Pelo fato do object ser response_object = False ele dá erro na hora da criação
        # Sendo necessário passar duas vezes pela função is_created, dessa maneira o try força
        #ele a retornar a essa página
        if user_base.is_created() is False:
            createUser = user_base.create_base()
            return HTTPFound(location=self.request.route_url("home_config_initial"))
        elif orgao_base.is_created() is False:
            createOrgao = orgao_base.create_base()
            return HTTPFound(location=self.request.route_url("home_config_initial"))
        elif notify_base.is_created() is False:
            createNotify = notify_base.create_base()
            return HTTPFound(location=self.request.route_url("home_config_initial"))
        elif atividade_base.is_created() is False:
            createAtividade = atividade_base.create_base()
            return HTTPFound(location=self.request.route_url("home_config_initial"))
        else:
            return HTTPFound(location=self.request.route_url("home"))

    #@view_config(route_name='home_config_initial', renderer='../templates/home_config_initial.pt')
    def home_config_initial(self):
        user_base = model_usuario.UserBase()
        orgao_base = model_orgao.OrgaoBase()
        notify_base = model_notify.NotifyBase()
        atividade_base = model_atividade.AtividadeBase()
        if user_base.is_created() is False:
            base_criada = "Criar Base de Usuário"
            return {'base_criada':base_criada}
        if orgao_base.is_created() is False:
            base_criada = "Criar Base de Órgãos"
            return {'base_criada':base_criada}
        if notify_base.is_created() is False:
            base_criada = "Criar Base de Notificações"
            return {'base_criada':base_criada}
        if atividade_base.is_created() is False:
            base_criada = "Criar Base de Atividades"
            return {'base_criada':base_criada}
        return HTTPFound(location=self.request.route_url("home"))

    #@view_config(route_name='home', renderer='../templates/home.pt')
    def home(self):
        # CONFIGURAÇÃO INICIAL
        user_base = model_usuario.UserBase()
        orgao_base = model_orgao.OrgaoBase()
        notify_base = model_notify.NotifyBase()
        atividade_base = model_atividade.AtividadeBase()
        if (user_base.is_created() is False or
            orgao_base.is_created() is False or
            notify_base.is_created() is False or
            atividade_base.is_created() is False
        ):
            return HTTPFound(location=self.request.route_url("home_config_initial"))
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        result_count = search.result_count
        if(result_count == 0):
            return HTTPFound(location=self.request.route_url("init_config_user"))
        # END CONFIGURAÇÃO INICIAL

        # RETORNA BASE DE RELATÓRIOS
        try:
            is_base_right = False
            base_list = Utils.return_all_bases_list()
            num_bases = len(base_list) - 1
            num_already_chosen = []
            while not is_base_right:
                chosen_base = base_list[randint(0, num_bases)]
                if chosen_base in num_already_chosen:
                    pass
                else:
                    base_obj = Utils.return_base_by_name(chosen_base)
                    is_coleta = Utils.is_base_coleta(base_obj)
                    if(is_coleta):
                        right_base = base_obj
                        is_base_right = True
            win32_bios = "win32_bios"
            win32_bios_manufacturer = "win32_bios_manufacturer"
            data = model_reports.Reports(chosen_base).count_attribute(win32_bios, win32_bios_manufacturer)
        except:
            data = None
        # END RETORNA BASE RELATÓRIOS

        # RETORNA BASE DE ATIVIDADES
        atividade_obj = Utils.create_atividade_obj()
        limit_registros = 10
        doc_atividade = atividade_obj.search_list_atividades(limit_registros)
        # END RETORNA BASE DE ATIVIDADES

        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {'usuario_autenticado': usuario_autenticado,
                'base_doc': data,
                'doc_atividade': doc_atividade.results
        }