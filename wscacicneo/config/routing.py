#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from ..views import home, notifications, orgaos, users, relatorios, coleta, security, api


def make_routes(cfg):
    """
    Cria rotas do Super Gerente
    """
    cfg.add_static_view('static', 'static', cache_max_age=3600)

    # Rotas de Configuração
    cfg.add_route('master', 'master', factory=home.Home)
    cfg.add_route('blankmaster', 'blankmaster', factory=home.Home)
    cfg.add_route('root', '/', factory=home.Home)
    cfg.add_route('create_config_initial', 'config_inicial', factory=home.Home)
    cfg.add_route('home_config_initial', 'home/config', factory=home.Home)

    # Rotas Básicas
    cfg.add_route('home', 'home', factory=home.Home)

    # Notificações
    cfg.add_route('notifications', 'notifications', factory=notifications.Notifications)

    # Orgãos
    cfg.add_route('orgao', 'orgao/cadastro', factory=orgaos.Orgaos)
    cfg.add_route('post_orgao', 'post_orgao', factory=orgaos.Orgaos)
    cfg.add_route('put_orgao', 'put_orgao', factory=orgaos.Orgaos)
    cfg.add_route('editorgao', 'orgao/editar/{sigla}', factory=orgaos.Orgaos)
    cfg.add_route('listorgao', 'orgao/lista', factory=orgaos.Orgaos)
    cfg.add_route('delete_orgao', 'orgao/delete/{sigla}', factory=orgaos.Orgaos)
    cfg.add_route('base_de_dados', 'orgao/base/{sigla}', factory=orgaos.Orgaos)
    cfg.add_route('config_orgao', 'orgao/configuracoes/{sigla}', factory=orgaos.Orgaos)

    # Users
    cfg.add_route('user', 'usuario/cadastro', factory=users.Users)
    cfg.add_route('post_user', 'post_user', factory=users.Users)
    cfg.add_route('post_first_user', 'post_first_user', factory=users.Users)
    cfg.add_route('put_user', 'put_user', factory=users.Users)
    cfg.add_route('edituser', 'usuario/editar/{matricula}', factory=users.Users)
    cfg.add_route('favoritos', 'usuario/favoritos/{matricula}', factory=users.Users)
    cfg.add_route('edit_favoritos', 'edit_favoritos', factory=users.Users)
    cfg.add_route('listuser', 'usuario/lista', factory=users.Users)
    cfg.add_route('delete_user', 'usuario/delete/{matricula}', factory=users.Users)
    cfg.add_route('notify', 'notificacoes/cadastro', factory=users.Users)
    cfg.add_route('post_notify', 'post_notify', factory=users.Users)
    cfg.add_route('delete_notify', 'delete_notify/{orgao}', factory=users.Users)
    cfg.add_route('edit_notify', 'edit_notify/{orgao}', factory=users.Users)
    cfg.add_route('list_notify', 'notificacoes/lista', factory=users.Users)
    cfg.add_route('edit_profile_user', 'usuario/perfil/{matricula}', factory=users.Users)
    cfg.add_route('edit_password_user', 'usuario/perfil/senha/{matricula}', factory=users.Users)
    cfg.add_route('put_password_user', 'put_password_user', factory=users.Users)
    cfg.add_route('put_profile_user', 'put_profile_user', factory=users.Users)
    cfg.add_route('init_config_user', 'configuracao_inicial/usuario', factory=users.Users)

    # Base de Rerpot por Orgãos
    cfg.add_route('create_orgao', 'create/coleta/{nm_orgao}', factory=coleta.Coleta)

    # Relatórios
    cfg.add_route('conf_report', 'relatorios/configuracao', factory=relatorios.Relatorios)
    cfg.add_route('report_itens', 'relatorio/{nm_orgao}/{attr}/{child}', factory=relatorios.Relatorios)

    # Coleta Manual
    cfg.add_route('cadastro_coleta', 'coleta/cadastro', factory=coleta.Coleta)
    cfg.add_route('post_coleta_manual', 'post_coleta_manual', factory=coleta.Coleta)

    # Autenticação
    cfg.add_route('login', 'login', factory=security.Security)
    cfg.add_route('logout', 'logout', factory=security.Security)

    # REST API
    cfg.add_route('orgao_config', 'api/orgaos/{orgao}', request_method='GET', factory=api.Api)
    cfg.add_route('orgao_coleta', 'api/{orgao}', request_method='GET', factory=api.Api)
    cfg.add_route('orgao_relatorio', 'api/{orgao}/relatorios', request_method='GET', factory=api.Api)