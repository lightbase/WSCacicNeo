#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from ..views import home, notifications, orgaos, users, relatorios, coleta, security, api, graficos


def make_routes(cfg):
    """
    Cria rotas do Super Gerente
    """
    cfg.add_static_view('static', 'static', cache_max_age=3600)

    # Rotas de Configuração
    cfg.add_route('master', 'master')
    cfg.add_view(home.Home, attr='master', route_name='master',
                 renderer='templates/blankmaster.pt')

    cfg.add_route('blankmaster', 'blankmaster')
    cfg.add_view(home.Home, attr='blankmaster', route_name='blankmaster',
                 renderer='templates/master.pt')

    cfg.add_route('root', '/')
    cfg.add_view(home.Home, attr='root', route_name='root')

    cfg.add_route('create_config_initial', 'config_inicial')
    cfg.add_view(home.Home, attr='create_config_initial', route_name='create_config_initial')

    cfg.add_route('home_config_initial', 'home/config')
    cfg.add_view(home.Home, attr='home_config_initial', route_name='home_config_initial',
                 renderer='templates/home_config_initial.pt')

    # Rotas Básicas
    cfg.add_route('home', 'home')
    cfg.add_view(home.Home, attr='home', route_name='home',
                 renderer='templates/home.pt')

    # Notificações
    cfg.add_route('notifications', 'notifications')
    cfg.add_view(notifications.Notifications, attr='notifications', route_name='notifications')

    # Orgãos
    cfg.add_route('orgao_initial', 'orgao_inicial')
    cfg.add_view(orgaos.Orgaos, attr='post_orgao_initial', route_name='orgao_initial', request_method='POST')
    cfg.add_view(orgaos.Orgaos, attr='get_orgao_initial', route_name='orgao_initial',
                 renderer='templates/orgao_initial.pt', request_method='GET')

    cfg.add_route('orgao', 'orgao/cadastro')
    cfg.add_view(orgaos.Orgaos, attr='orgao', route_name='orgao',
                 renderer='templates/orgao.pt', permission="admin")

    cfg.add_route('post_orgao', 'post_orgao')
    cfg.add_view(orgaos.Orgaos, attr='post_orgao', route_name='post_orgao',
                 renderer='templates/config_orgao.pt', permission="admin")

    cfg.add_route('put_orgao', 'put_orgao')
    cfg.add_view(orgaos.Orgaos, attr='put_orgao', route_name='put_orgao',
                 permission="admin")

    cfg.add_route('editorgao', 'orgao/editar/{sigla}')
    cfg.add_view(orgaos.Orgaos, attr='editorgao', route_name='editorgao',
                 renderer='templates/editarorgao.pt', permission="admin")

    cfg.add_route('listorgao', 'orgao/lista')
    cfg.add_view(orgaos.Orgaos, attr='listorgao', route_name='listorgao',
                 renderer='templates/list_orgao.pt', permission="admin")

    cfg.add_route('delete_orgao', 'orgao/delete/{sigla}')
    cfg.add_view(orgaos.Orgaos, attr='delete_orgao', route_name='delete_orgao',
                 permission="admin")

    cfg.add_route('base_de_dados', 'orgao/base/{sigla}')
    cfg.add_view(orgaos.Orgaos, attr='base_de_dados', route_name='base_de_dados',
                 permission="admin")

    cfg.add_route('config_orgao', 'orgao/configuracoes/{sigla}')
    cfg.add_view(orgaos.Orgaos, attr='config_orgao', route_name='config_orgao',
                 renderer='templates/config_orgao.pt', permission="admin")

    # Users
    cfg.add_route('user', 'usuario/cadastro')
    cfg.add_view(users.Users, attr='user', route_name='user',
                 renderer='templates/user.pt', permission='admin')

    cfg.add_route('post_user', 'post_user')
    cfg.add_view(users.Users, attr='post_user', route_name='post_user',
                 permission="admin")

    cfg.add_route('post_first_user', 'post_first_user')
    cfg.add_view(users.Users, attr='post_first_user', route_name='post_first_user')

    cfg.add_route('put_user', 'put_user')
    cfg.add_view(users.Users, attr='put_user', route_name='put_user',
                 permission='admin')

    cfg.add_route('edituser', 'usuario/editar/{matricula}')
    cfg.add_view(users.Users, attr='edituser', route_name='edituser',
                 renderer='templates/editaruser.pt', permission='admin')

    cfg.add_route('favoritos', 'usuario/favoritos/{matricula}')
    cfg.add_view(users.Users, attr='favoritos', route_name='favoritos',
                 renderer='templates/favoritos.pt', permission="gest")

    cfg.add_route('edit_favoritos', 'edit_favoritos')
    cfg.add_view(users.Users, attr='edit_favoritos', route_name='edit_favoritos',
                 permission="gest")

    cfg.add_route('listuser', 'usuario/lista')
    cfg.add_view(users.Users, attr='listuser', route_name='listuser',
                 renderer='templates/list_user.pt', permission="admin")

    cfg.add_route('delete_user', 'usuario/delete/{matricula}')
    cfg.add_view(users.Users, attr='delete_user', route_name='delete_user',
                 permission="admin")

    cfg.add_route('notify', 'notificacoes/cadastro')
    cfg.add_view(notifications.Notifications, attr='notify', route_name='notify',
                 renderer='templates/notify_coleta.pt', permission="gest")

    cfg.add_route('post_notify', 'post_notify')
    cfg.add_view(notifications.Notifications, attr='post_notify', route_name='post_notify',
                 permission="gest")

    cfg.add_route('delete_notify', 'delete_notify/{orgao}')
    cfg.add_view(notifications.Notifications, attr='delete_notify', route_name='delete_notify',
                 permission='gest')

    cfg.add_route('edit_notify', 'edit_notify/{orgao}')
    cfg.add_view(notifications.Notifications, attr='edit_notify', route_name='edit_notify',
                 permission="gest")

    cfg.add_route('list_notify', 'notificacoes/lista')
    cfg.add_view(notifications.Notifications, attr='list_notify', route_name='list_notify',
                 permission="gest", renderer='templates/list_notify.pt')

    cfg.add_route('notify_count', 'notificacoes/contagem')
    cfg.add_view(notifications.Notifications, attr='count_notify', route_name='notify_count',
                 permission="gest")

    cfg.add_route('edit_profile_user', 'usuario/perfil/{matricula}')
    cfg.add_view(users.Users, attr='edit_profile_user', route_name='edit_profile_user',
                 renderer='templates/editarperfil.pt', permission="gest")

    cfg.add_route('edit_password_user', 'usuario/perfil/senha/{matricula}')
    cfg.add_view(users.Users, attr='edit_password_user', route_name='edit_password_user',
                 renderer='templates/alterar_senha.pt', permission="gest")

    cfg.add_route('put_password_user', 'put_password_user')
    cfg.add_view(users.Users, attr='put_password_user', route_name='put_password_user',
                 permission="gest")

    cfg.add_route('put_profile_user', 'put_profile_user')
    cfg.add_view(users.Users, attr='put_profile_user', route_name='put_profile_user',
                 permission="gest")

    cfg.add_route('init_config_user', 'configuracao_inicial/usuario')
    cfg.add_view(users.Users, attr='init_config_user', route_name='init_config_user',
                 renderer='templates/init_config_user.pt')

    # Base de Rerpot por Orgãos
    cfg.add_route('create_orgao', 'create/coleta/{nm_orgao}')
    cfg.add_view(coleta.Coleta, attr='create_orgao', route_name='create_orgao',
                 permission="gest")

    # Coleta Manual
    cfg.add_route('cadastro_coleta', 'coleta/cadastro')
    cfg.add_view(coleta.Coleta, attr='cadastro_coleta', route_name='cadastro_coleta',
                 renderer='templates/cadastro_coleta.pt', permission="gest")

    cfg.add_route('post_coleta_manual', 'post_coleta_manual')
    cfg.add_view(coleta.Coleta, attr='post_coleta_manual', route_name='post_coleta_manual',
                 permission="gest")

    # Relatórios
    cfg.add_route('conf_report', 'relatorios/configuracao')
    cfg.add_view(relatorios.Relatorios, attr='conf_report', route_name='conf_report',
                 renderer='templates/conf_report.pt')

    cfg.add_route('report_itens', 'relatorio/{nm_orgao}/{attr}/{child}')
    cfg.add_view(relatorios.Relatorios, attr='report_itens', route_name='report_itens',
                 renderer='templates/report.pt', permission="user")

    cfg.add_route('put_reports', 'put_reports')
    cfg.add_view(relatorios.Relatorios, attr='put_reports', route_name='put_reports',
                  permission="user")
    # Gráficos
    cfg.add_route('graficos', 'graficos/{nm_orgao}/{attr}')
    cfg.add_view(graficos.Graficos, attr='graficos', route_name='graficos',
                 renderer='templates/graficos/graficos.pt')

    cfg.add_route('report_software', 'relatorio/software/{nm_orgao}')
    cfg.add_view(relatorios.Relatorios, attr='report_software', route_name='report_software',
                 renderer='templates/report.pt', permission="user")

    # Autenticação
    cfg.add_route('login', 'login')
    cfg.add_view(security.Security, attr='login', route_name='login',
                 renderer='templates/login.pt')
    cfg.add_forbidden_view(security.Security, renderer='templates/login.pt')

    cfg.add_route('logout', 'logout')
    cfg.add_view(security.Security, attr='logout', route_name='logout',
                 permission="user")

    # REST API
    cfg.add_route('orgao_config', 'api/orgaos/{orgao}', request_method='GET')
    cfg.add_view(api.Api, attr='orgao_config', route_name='orgao_config',
                 permission='user')

    cfg.add_route('orgao_create', 'api/{orgao}', request_method='POST')
    cfg.add_view(api.Api, attr='orgao_create', route_name='orgao_create',
                 permission='user')

    cfg.add_route('orgao_remove', 'api/{orgao}', request_method='DELETE')
    cfg.add_view(api.Api, attr='orgao_remove', route_name='orgao_remove',
                 permission='user')

    cfg.add_route('orgao_upload', 'api/{orgao}/upload', request_method='POST')
    cfg.add_view(api.Api, attr='orgao_upload', route_name='orgao_upload',
                 permission='user')

    # Rotas públicas
    cfg.add_route('orgao_coleta', 'api/{orgao}', request_method='GET')
    cfg.add_view(api.Api, attr='orgao_coleta', route_name='orgao_coleta')

    cfg.add_route('orgao_relatorio', 'api/{orgao}/relatorios', request_method='GET')
    cfg.add_view(api.Api, attr='orgao_relatorio', route_name='orgao_relatorio')
