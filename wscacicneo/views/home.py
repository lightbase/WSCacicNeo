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
from wscacicneo.model import config_reports
from wscacicneo import config
from liblightbase.lbsearch.search import NullDocument
from pyramid.security import (
    remember,
    forget,
    )

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
        if not Utils.check_has_orgao():
            return HTTPFound(location=self.request.route_url("orgao_initial"))
        if not Utils.check_has_user():
            return HTTPFound(location=self.request.route_url("init_config_user"))
        # END CONFIGURAÇÃO INICIAL

        """# RETORNA BASE DE RELATÓRIOS
        base_list = Utils.return_all_bases_list()
        right_base = None
        for base in base_list:
            base_obj = Utils.return_base_by_name(base)
            is_coleta = Utils.is_base_coleta(base_obj)
            print(base)
            if is_coleta and "_bk" not in base:
                right_base = base
                print(right_base)
                break

        win32_bios = "win32_bios"
        win32_bios_manufacturer = "win32_bios_manufacturer"
        data = model_reports.Reports(right_base).count_attribute(win32_bios, win32_bios_manufacturer)
        # END RETORNA BASE RELATÓRIOS"""
        data = None

        # RETORNA BASE DE ATIVIDADES
        atividade_obj = Utils.create_atividade_obj()
        limit_registros = 5
        doc_atividade = atividade_obj.search_list_atividades(limit_registros)
        # END RETORNA BASE DE ATIVIDADES


        usuario_autenticado = Utils.retorna_usuario_autenticado(
            email=self.request.authenticated_userid)

        # Relatórios personalizados
        report_data = [ ]
        if usuario_autenticado and hasattr(usuario_autenticado.results[0], 'home'):
            for home_report_attr in set(usuario_autenticado.results[0].home):
                report_data.append(
                    (home_report_attr, self.get_user_report_data_by_attr(
                    usuario_autenticado.results[0], home_report_attr))
                )
        session = self.request.session
        return {'usuario_autenticado': usuario_autenticado,
                'base_doc': data,
                'doc_atividade': doc_atividade.results,
                'report_data': report_data,
        }

    def get_user_report_data_by_attr(self, user, attr):
        if attr == 'software':
            attr = 'softwarelist'
        reports_config = config_reports.ConfReports(user.orgao)
        results = reports_config.get_attribute(attr).results
        report_data = dict()
        for elm in results:
            if isinstance(elm, NullDocument):
                continue
            parent = getattr(elm, attr)
            item = getattr(parent, attr + '_item')
            amount = getattr(parent, attr + '_amount')
            report_data[item] = amount
        return report_data
