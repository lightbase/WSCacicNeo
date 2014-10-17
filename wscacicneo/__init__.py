#!/usr/env python
# -*- coding: utf-8 -*-

from wscacicneo import config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config.setup(settings)
    from wscacicneo.security import groupfinder
    authn_policy = AuthTktAuthenticationPolicy(
    'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    cfg = Configurator(settings=settings, root_factory='wscacicneo.models.RootFactory')
    cfg.set_authentication_policy(authn_policy)
    cfg.set_authorization_policy(authz_policy)

    cfg.include('pyramid_chameleon')
    cfg.add_static_view('static', 'static', cache_max_age=3600)

    # Rotas de Configuração
    cfg.add_route('master', 'master')
    cfg.add_route('blankmaster', 'blankmaster')
    cfg.add_route('root', '/')

    # Rotas Básicas
    cfg.add_route('home', 'home')
    cfg.add_route('notifications', 'notifications')
    cfg.add_route('orgao', 'orgao/cadastro')
    
    # Orgãos
    cfg.add_route('post_orgao', 'post_orgao')
    cfg.add_route('put_orgao', 'put_orgao')
    cfg.add_route('editorgao', 'orgao/editar/{sigla}')
    cfg.add_route('listorgao', 'orgao/lista')
    cfg.add_route('delete_orgao', 'orgao/delete/{sigla}')
    cfg.add_route('base_de_dados', 'orgao/base/{sigla}')
    
    # Users
    cfg.add_route('user', 'usuario/cadastro')
    cfg.add_route('post_user', 'post_user')
    cfg.add_route('put_user', 'put_user')
    cfg.add_route('edituser', 'usuario/editar/{matricula}')
    cfg.add_route('favoritos', 'usuario/favoritos/{matricula}')
    cfg.add_route('edit_favoritos', 'edit_favoritos')
    cfg.add_route('listuser', 'usuario/lista')
    cfg.add_route('delete_user', 'usuario/delete/{matricula}')
    cfg.add_route('notify', 'notificacoes/cadastro')
    cfg.add_route('post_notify', 'post_notify')
    cfg.add_route('list_notify', 'notificacoes/lista')
    
    # Base de Rerpot por Orgãos
    cfg.add_route('create_orgao', 'create/orgao/{nm_orgao}')
    
    # Relatórios
    cfg.add_route('conf_report', 'relatorios/configuracao')
    cfg.add_route('report_itens', 'relatorio/{nm_orgao}/{attr}/{child}')
    
    # Coleta Manual
    cfg.add_route('cadastro_coleta', 'coleta/cadastro')
    cfg.add_route('post_coleta_manual', 'post_coleta_manual')
    
    # Autenticação
    cfg.add_route('login', 'login')
    cfg.add_route('logout', 'logout')
    
    cfg.scan()
    return cfg.make_wsgi_app()
