#!/usr/env python
# -*- coding: utf-8 -*-

from wscacicneo import config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator



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
    cfg.add_route('master', 'master')
    cfg.add_route('blankmaster', 'blankmaster')
    cfg.add_route('root', '/')

    cfg.add_route('home', 'home')
    cfg.add_route('graficop', 'graficop')
    cfg.add_route('notifications', 'notifications')
    cfg.add_route('admin', 'admin')
    cfg.add_route('proc', 'proc')
    cfg.add_route('sistema', 'sistema')
    cfg
    cfg.add_route('orgao', 'orgao/cadastro')
    cfg.add_route('post_orgao', 'post_orgao')
    cfg.add_route('put_orgao', 'put_orgao')
    cfg.add_route('editorgao', 'orgao/editar/{sigla}')
    cfg.add_route('listorgao', 'orgao/lista')
    cfg.add_route('delete_orgao', 'orgao/delete/{sigla}')
    cfg.add_route('base_de_dados', 'orgao/base/{sigla}')
    #
    cfg.add_route('user', 'usuario/cadastro')
    cfg.add_route('post_user', 'post_user')
    cfg.add_route('put_user', 'put_user')
    cfg.add_route('edituser', 'usuario/editar/{matricula}')
    cfg.add_route('favoritos', 'usuario/favoritos/{matricula}')
    cfg.add_route('edit_favoritos', 'edit_favoritos')
    cfg.add_route('listuser', 'usuario/lista')
    cfg.add_route('delete_user', 'usuario/delete/{matricula}')
    cfg.add_route('notify', 'lista/notificacoes')
    cfg.add_route('post_notify', 'post_notify')
    #
    cfg.add_route('list', 'list')
    cfg.add_route('gestao', 'gestao')
    cfg.add_route('memoria', 'memoria')
    cfg.add_route('basico', 'basico')
    cfg.add_route('rede', 'rede')
    cfg.add_route('escritorio', 'escritorio')
    cfg.add_route('hd', 'hd')
    cfg.add_route('config', 'config')
    cfg.add_route('bot', 'bot')
    cfg.add_route('login', 'login')
    cfg.add_route('loginautentication', 'loginautentication')
    cfg.add_route('logout', 'logout')
    cfg.add_route('reports', 'reports')
    cfg.add_route('computador', 'computador')
    cfg.add_route('busca', 'busca')
    cfg.add_route('gestor', 'gestor')
    cfg.add_route('diagnostic', 'diagnostic')
    cfg.add_route('cadastro', 'cadastro')
    cfg.add_route('sobre', 'sobre')
    cfg.add_route('perfil', 'perfil')
    cfg.add_route('configapi','configapi')
    cfg.add_route('processador','processador')
    cfg.add_route('configcoleta','configcoleta')
    cfg.add_route('configfav','configfav')
    cfg.add_route('reportsgestor','reportsgestor')
    cfg.add_route('questionarcoleta','questionarcoleta')
    cfg.add_route('confighome','confighome')
    cfg.add_route('db','db')
    cfg.scan()
    return cfg.make_wsgi_app()
