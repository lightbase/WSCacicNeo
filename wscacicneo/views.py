#!/usr/env python
# -*- coding: utf-8 -*-
import requests
import json
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from wscacicneo.utils.utils import Utils
from wscacicneo.model.orgao import Orgao
from wscacicneo.model import orgao as model_orgao
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from wscacicneo.model.user import User
from wscacicneo.model import user as model_usuario
from wscacicneo.model.reports import Reports
from wscacicneo.model.notify import Notify
from wscacicneo.model import notify as model_notify
from wscacicneo.model import coleta_manual
from wscacicneo.model.reports import Reports
from wscacicneo.model import base_bk as model_base_bk

from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from liblightbase.lbrest.document import DocumentREST
from pyramid.view import forbidden_view_config

from pyramid.security import (
    remember,
    forget,
    )

REST_URL = 'http://api.brlight.net/api'


# Views de configuração
@view_config(route_name='blankmaster', renderer='templates/blankmaster.pt')
def blankmaster(request):
    return HTTPFound(location=request.route_url("home"))

@view_config(route_name='master', renderer='templates/master.pt')
def master(request):
    return HTTPFound(location=request.route_url("home"))

@view_config(route_name='root')
def root(request):
    return HTTPFound(location=request.route_url("home"))

# Views básicas
@view_config(route_name='create_config_initial')
def create_config_initial(request):
    user_base = model_usuario.UserBase()
    orgao_base = model_orgao.OrgaoBase()
    notify_base = model_notify.NotifyBase()
    # Cria tudo que precisa para carregar.
    # Pelo fato do object ser response_object = False ele dá erro na hora da criação
    # Sendo necessário passar duas vezes pela função is_created, dessa maneira o try força
    #ele a retornar a essa página
    try:
        if (user_base.is_created() == False):
            createUser = user_base.create_base()
        if (orgao_base.is_created() == False):
            createOrgao = orgao_base.create_base()
        if (notify_base.is_created() == False):
            createNotify = notify_base.create_base()
    except:
        return HTTPFound(location=request.route_url("home_config_initial"))

@view_config(route_name='home_config_initial', renderer='templates/home_config_initial.pt')
def home_config_initial(request):
    user_base = model_usuario.UserBase()
    orgao_base = model_orgao.OrgaoBase()
    notify_base = model_notify.NotifyBase()
    if (user_base.is_created() == False ):
        base_criada = "Criar Base de Usuário"
        return {'base_criada':base_criada}
    if (orgao_base.is_created() == False):
        base_criada = "Criar Base de Órgãos"
        return {'base_criada':base_criada}
    if (notify_base.is_created() == False):
        base_criada = "Criar Base de Notificações"
        return {'base_criada':base_criada}
    return HTTPFound(location=request.route_url("home"))

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    #CONFIGURAÇÃO INICIAL
    user_base = model_usuario.UserBase()
    orgao_base = model_orgao.OrgaoBase()
    notify_base = model_notify.NotifyBase()
    if (user_base.is_created() == False or orgao_base.is_created() == False or notify_base.is_created() == False):
        return HTTPFound(location=request.route_url("home_config_initial"))
    #END CONFIGURAÇÃO INICIAL
    user_obj = Utils.create_user_obj()
    search = user_obj.search_list_users()
    result_count = search.result_count
    if(result_count == 0):
        return HTTPFound(location=request.route_url("init_config_user"))
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    # bases = requests.get("http://127.0.0.1/lbgenerator/")
    # print(1111111111111111111111111111111111111111111111111111111,bases.text)
    return {'usuario_autenticado':usuario_autenticado}

# Lista de Notificação
@view_config(route_name='list_notify', renderer='templates/list_notify.pt', permission="gest")
def list_notify(request):
    notify_obj = Notify(
        orgao = 'deasdsd',
        data_coleta = 'saudhasd',
        notify = 'sadsad',
        coment = 'sadasd',
        status = 'sadasd'
    )
    reg = notify_obj.search_list_notify()
    doc = reg.results
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {'doc': doc,
            'usuario_autenticado':usuario_autenticado
            }

@view_config(route_name='delete_notify', permission="gest")
def delete_notify(request):
    orgao = request.matchdict['orgao']
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
    return HTTPFound(location = request.route_url('list_notify'))

@view_config(route_name='edit_notify', permission="gest")
def edit_notify(request):
    orgao = request.matchdict['orgao']
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
    return HTTPFound(location = request.route_url('list_notify'))


@view_config(route_name='notify', renderer='templates/notify_coleta.pt', permission="gest")
def notify(request):
    orgao_obj = Orgao(
        nome = 'sahuds',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)

    return {'orgao_doc': search.results,
            'usuario_autenticado':usuario_autenticado
            }

@view_config(route_name='post_notify', permission="gest")
def post_notify(request):
    requests = request.params
    notify_obj = Notify(
        orgao = requests['orgao'],
        data_coleta = requests['data_coleta'],
        notify = requests['notify'],
        coment = requests['coment'],
        status = requests['status']
    )
    results = notify_obj.create_notify()
    return Response(str(results))

# Views de Orgão
@view_config(route_name='orgao', renderer='templates/orgao.pt', permission="admin")
def orgao(request):
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {'usuario_autenticado':usuario_autenticado}

@view_config(route_name='listorgao', renderer='templates/list_orgao.pt', permission="admin")
def listorgao(request):
    orgao_obj = Orgao(
        nome = 'sahuds',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {'orgao_doc': search.results,
            'usuario_autenticado':usuario_autenticado
            }

@view_config(route_name='config_orgao', renderer='templates/config_orgao.pt', permission="admin")
def config_orgao(request):
    sigla = request.matchdict['sigla']
    orgao_obj = Orgao(
        nome = 'asdsad',
        cargo = 'cargo',
        coleta = '4h',
        sigla = sigla,
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_orgao(sigla)
    usuario_autenticado = Utils.retorna_usuario_autenticado(request.authenticated_userid)

    return {
        'nome' : search.results[0].nome,
        'cargo' : search.results[0].cargo,
        'sigla' : search.results[0].sigla,
        'endereco' : search.results[0].endereco,
        'email' : search.results[0].email,
        'telefone' : search.results[0].telefone,
        'usuario_autenticado':usuario_autenticado
    }

@view_config(route_name='editorgao', renderer='templates/editarorgao.pt', permission="admin")
def editorgao(request):
    sigla = request.matchdict['sigla']
    orgao_obj = Orgao(
        nome = 'asdsad',
        cargo = 'cargo',
        coleta = '4h',
        sigla = sigla,
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_orgao(sigla)
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    
    return {
        'nome' : search.results[0].nome,
        'cargo' : search.results[0].cargo,
        'coleta' : search.results[0].coleta,
        'sigla' : search.results[0].sigla,
        'endereco' : search.results[0].endereco,
        'email' : search.results[0].email,
        'telefone' : search.results[0].telefone,
        'url' : search.results[0].url,
        'usuario_autenticado':usuario_autenticado
    }

@view_config(route_name='post_orgao', permission="admin")
def post_orgao(request):
    """
    Post doc órgãos
    """
    rest_url = REST_URL
    orgaobase = model_orgao.OrgaoBase().lbbase
    doc = request.params
    orgao_obj = Orgao(
        nome = doc['nome'],
        cargo = doc['gestor'],
        coleta = doc['coleta'],
        sigla = doc['sigla'],
        endereco = doc['end'],
        email = doc['email'],
        telefone = doc['telefone'],
        url = doc['url']
    )
    id_doc = orgao_obj.create_orgao()
    return Response(str(id_doc))

@view_config(route_name='put_orgao', permission="admin")
def put_orgao(request):
    """
    Edita um doc apartir do id
    """
    params = request.params
    sigla = params['id']
    orgao_obj = Orgao(
        nome = params['nome'],
        cargo = params['gestor'],
        coleta = params['coleta'],
        sigla = params['sigla'],
        endereco = params['end'],
        email = params['email'],
        telefone = params['telefone'],
        url = params['url']
    )
    orgao = {
        'nome' : params['nome'],
        'cargo' : params['gestor'],
        'coleta' : params['coleta'],
        'sigla' : params['sigla'],
        'endereco' : params['end'],
        'email' : params['email'],
        'telefone' : params['telefone'],
        'url' : params['url']
    }
    search = orgao_obj.search_orgao(sigla)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(orgao)
    edit = orgao_obj.edit_orgao(id, doc)
    return Response(edit)

@view_config(route_name='delete_orgao', permission="admin")
def delete_orgao(request):
    """
    Deleta doc apartir do id
    """
    doc = request.params
    sigla = request.matchdict['sigla']
    orgao_obj = Orgao(
        nome = 'asdasd',
        cargo = 'asdasdasd',
        coleta = 'asdasdasd',
        sigla = 'asdasdas',
        endereco = 'asdsad',
        email = 'asdsad',
        telefone = 'sadasd',
        url = 'sadasd'
    )
    search = orgao_obj.search_orgao(sigla)
    id = search.results[0]._metadata.id_doc
    delete = orgao_obj.delete_orgao(id)
    return HTTPFound(location = request.route_url('listorgao'))

# Views de Favoritos
@view_config(route_name='favoritos', renderer='templates/favoritos.pt', permission="gest")
def favoritos(request):
    matricula = request.matchdict['matricula']
    user_obj = Utils.create_user_obj()
    search = user_obj.search_user(matricula)
    email = search.results[0].email
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    if (usuario_autenticado.results[0].email ==  email):
        search = user_obj.search_user(matricula)
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
        favoritos = search.results[0].favoritos
        return {
            'favoritos': search.results[0].favoritos,
            'itens': search.results[0].itens,
            'nome' : search.results[0].nome,
            'matricula' : search.results[0].matricula,
            'email' : search.results[0].email,
            'orgao' : search.results[0].orgao,
            'telefone' : search.results[0].telefone,
            'cargo' : search.results[0].cargo,
            'setor' : search.results[0].setor,
            'permissao' : search.results[0].permissao,
            'senha' : search.results[0].senha,
            'usuario_autenticado':usuario_autenticado
        }
    else:
        return HTTPFound(location = request.route_url('home'))

@view_config(route_name='edit_favoritos', permission="gest")
def edit_favoritos(request):
    """
    Editar do Favoritos
    """
    documento = json.loads(request.params['documento'])
    matricula = documento['matricula']
    user_obj = User(
        nome = documento['nome'],
        matricula = documento['matricula'],
        email = documento['email'],
        orgao = documento['orgao'],
        telefone = documento['telefone'],
        cargo = documento['cargo'],
        setor = documento['setor'],
        permissao = documento['permissao'],
        senha = documento['senha']
    )
    user = {
        'nome' : documento['nome'],
        'matricula' : documento['matricula'],
        'email' : documento['email'],
        'orgao' : documento['orgao'],
        'telefone' : documento['telefone'],
        'cargo' : documento['cargo'],
        'setor' : documento['setor'],
        'permissao' : documento['permissao'],
        'senha' : documento['senha'],
        'itens': documento['itens'],
        'favoritos': documento['favoritos']
    }
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(user)
    edit = user_obj.edit_user(id, doc)
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return Response(edit)

# Reports
@view_config(route_name='create_orgao',permission="gest")
def create_base(request):
    nm_orgao = Utils.format_name(request.matchdict['nm_orgao'])
    coletaManualBase = coleta_manual.ColetaManualBase(nm_orgao)
    lbbase = coletaManualBase.lbbase
    retorno = coletaManualBase.create_base()
    return Response(retorno)

@view_config(route_name='conf_report', renderer='templates/conf_report.pt')
def conf_report(request):
    orgao_obj = Orgao(
        nome = 'sahuds',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)

    return {'orgao_doc': search.results,
            'usuario_autenticado':usuario_autenticado
            }

@view_config(route_name='report_itens', renderer='templates/report.pt', permission="user")
def report_itens(request):
    orgao_nm = request.matchdict['nm_orgao']
    nm_orgao = Utils.format_name(orgao_nm)
    report_base = base_reports.ReportsBase(nm_orgao)
    if(report_base.is_created() == False):
        create_base = report_base.create_base()
        attr = request.matchdict['attr']
        child = request.matchdict['child']
        data = Reports(nm_orgao).count_attribute(attr, child)
        reports_config = config_reports.ConfReports(nm_orgao)
        for items in data:
            data_json = {attr : { attr+'_item' : items, attr+'_amount': str(data[items])}}
            document = json.dumps(data_json)
            reports_config.create_coleta(document)
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
        return {'data': data,
                'status_base': create_base,
                'usuario_autenticado':usuario_autenticado
                }
    else:
        orgao_nm = request.matchdict['nm_orgao']
        nm_orgao = Utils.format_name(orgao_nm)
        attr = request.matchdict['attr']
        child = request.matchdict['child']
        data = Reports(nm_orgao).count_attribute(attr, child)
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
        return {
                'data': data,
                'usuario_autenticado':usuario_autenticado
                }

# Users

@view_config(route_name='user', renderer='templates/user.pt', permission='admin')
def user(request):
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {'usuario_autenticado':usuario_autenticado}

@view_config(route_name='post_user', permission="admin")
def post_user(request):
    """
    Post doc users
    """
    rest_url = REST_URL
    userbase = model_usuario.UserBase().lbbase
    doc = request.params
    email_user = doc['email']
    email_is_institucional = Utils.verifica_email_institucional(email_user)
    if(email_is_institucional):
        document = doc['favoritos']
        favoritos = [document]
        if(doc['permissao'] == "Administrador "):
            itens = [doc['lista_orgao'], doc['cadastro_orgao'], doc['lista_user'], doc['cadastro_user'], doc['notify']]
        else:
            itens = [doc['notify']]
        user_obj = User(
            nome = doc['nome'],
            matricula = doc['matricula'],
            email = doc['email'],
            orgao = doc['orgao'],
            telefone = doc['telefone'],
            cargo = doc['cargo'],
            setor = doc['setor'],
            permissao = doc['permissao'],
            senha = Utils.hash_password(doc['senha']),
            favoritos = favoritos,
            itens = itens
        )
        id_doc = user_obj.create_user()

        return Response(str(id_doc))
    else:
        return {"emailerrado":"emailerrado"}

@view_config(route_name='post_first_user')
def post_first_user(request):
    """
    Post doc users
    """
    user_obj = Utils.create_user_obj()
    search = user_obj.search_list_users()
    result_count = search.result_count
    if(result_count == 0):
        rest_url = REST_URL
        userbase = model_usuario.UserBase().lbbase
        doc = request.params
        email_user = doc['email']
        email_is_institucional = Utils.verifica_email_institucional(email_user)
        if(email_is_institucional):
            document = doc['favoritos']
            favoritos = [document]
            itens = [doc['lista_orgao'], doc['cadastro_orgao'], doc['lista_user'], doc['cadastro_user'], doc['notify']]
            user_obj = User(
                nome = doc['nome'],
                matricula = doc['matricula'],
                email = doc['email'],
                orgao = doc['orgao'],
                telefone = doc['telefone'],
                cargo = doc['cargo'],
                setor = doc['setor'],
                permissao = "Administrador",
                senha = Utils.hash_password(doc['senha']),
                favoritos = favoritos,
                itens = itens
            )
            id_doc = user_obj.create_user()

            return Response(str(id_doc))
        else:
            return {"emailerrado":"emailerrado"}
    else:
        return HTTPFound(location = request.route_url('home')) 

@view_config(route_name='edituser', renderer='templates/editaruser.pt', permission="admin")
def edituser(request):
    matricula = request.matchdict['matricula']
    user_obj = Utils.create_user_obj()
    search = user_obj.search_user(matricula)
    email = search.results[0].email
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {
        'nome' : search.results[0].nome,
        'matricula' : search.results[0].matricula,
        'email' : search.results[0].email,
        'orgao' : search.results[0].orgao,
        'telefone' : search.results[0].telefone,
        'cargo' : search.results[0].cargo,
        'setor' : search.results[0].setor,
        'permissao' : search.results[0].permissao,
        'senha' : search.results[0].senha,
        'itens' : search.results[0].itens,
        'favoritos' : search.results[0].favoritos,
        'usuario_autenticado':usuario_autenticado,
    }

@view_config(route_name='put_user', permission="admin")
def put_user(request):
    """
    Edita um doc de user apartir do id
    """
    params = request.params
    matricula = params['url']
    email_user = params['email']
    user_obj = Utils.create_user_obj()
    search = user_obj.search_user(matricula)
    permissao_usuario_edit = search.results[0].permissao
    email_usuario_edit = search.results[0].email
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    usuario_autenticado_email = usuario_autenticado.results[0].email
    edit_yourself = False
    if(usuario_autenticado_email == email_usuario_edit):
        edit_yourself = True
        email_user = usuario_autenticado_email
    if(params['permissao'] == "Administrador" and params['permissao'] != permissao_usuario_edit):
        itens = [params['lista_orgao'], params['cadastro_orgao'], params['lista_user'], params['cadastro_user'], params['notify']]
        favoritos = [params['favoritos']]
        user = {
            'nome' : params['nome'],
            'matricula' : params['matricula'],
            'email' : params['email'],
            'orgao' : params['orgao'],
            'telefone' : params['telefone'],
            'cargo' : params['cargo'],
            'setor' : params['setor'],
            'permissao' : params['permissao'],
            'senha' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
            'favoritos' : favoritos,
            'itens' : itens
        }
    elif(params['permissao'] == "Gestor" and params['permissao'] != permissao_usuario_edit):
        itens = [params['notify']]
        favoritos = [params['favoritos']]
        user = {
            'nome' : params['nome'],
            'matricula' : params['matricula'],
            'email' : params['email'],
            'orgao' : params['orgao'],
            'telefone' : params['telefone'],
            'cargo' : params['cargo'],
            'setor' : params['setor'],
            'permissao' : params['permissao'],
            'senha' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
            'favoritos' : favoritos,
            'itens' : itens
        }
    else:
        user = {
            'nome' : params['nome'],
            'matricula' : params['matricula'],
            'email' : params['email'],
            'orgao' : params['orgao'],
            'telefone' : params['telefone'],
            'cargo' : params['cargo'],
            'setor' : params['setor'],
            'permissao' : params['permissao'],
            'senha' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
            'favoritos' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].favoritos,
            'itens' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].itens
        }
    id = search.results[0]._metadata.id_doc
    email_is_institucional = Utils.verifica_email_institucional(email_user)
    if(email_is_institucional):
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)
        if(edit_yourself == False):
            return Response(edit)
        else:
            headers = forget(request)
            response = Response()
            response = HTTPFound(location = request.route_url('login'),
                             headers = headers)
            return response
    else:
        return {"emailerrado":"E-mail não institucional"}

@view_config(route_name='listuser', renderer='templates/list_user.pt', permission="admin")
def listuser(request):
    user_obj = Utils.create_user_obj()
    search = user_obj.search_list_users()
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {'user_doc': search.results,
            'usuario_autenticado':usuario_autenticado
            }

@view_config(route_name='delete_user', permission="admin")
def delete_user(request):
    """
    Deleta doc apartir do id
    """
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    doc = request.params
    matricula = request.matchdict['matricula']
    user_obj = Utils.create_user_obj()
    search = user_obj.search_user(matricula)
    email = search.results[0].email
    if(usuario_autenticado.results[0].email !=  email):
        id = search.results[0]._metadata.id_doc
        delete = user_obj.delete_user(id)
        return HTTPFound(location = request.route_url('listuser'))
    else:
        return HTTPFound(location = request.route_url('listuser'))


@view_config(route_name='edit_profile_user', renderer='templates/editarperfil.pt', permission="gest")
def edit_profile_user(request):
    matricula = request.matchdict['matricula']
    user_obj = Utils.create_user_obj()
    search = user_obj.search_user(matricula)
    email = search.results[0].email
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    if (usuario_autenticado.results[0].email ==  email):
        return {
            'nome' : search.results[0].nome,
            'matricula' : search.results[0].matricula,
            'email' : search.results[0].email,
            'orgao' : search.results[0].orgao,
            'telefone' : search.results[0].telefone,
            'cargo' : search.results[0].cargo,
            'setor' : search.results[0].setor,
            'permissao' : search.results[0].permissao,
            'senha' : search.results[0].senha,
            'itens' : search.results[0].itens,
            'favoritos' : search.results[0].favoritos,
            'usuario_autenticado':usuario_autenticado,
        }
    else:
        return HTTPFound(location = request.route_url('home'))

@view_config(route_name='put_profile_user', permission="gest")
def put_profile_user(request):
    """
    Edita um doc de user apartir do id
    """
    params = request.params
    matricula = params['url']
    email_user_new = params['email']
    user_obj = Utils.create_user_obj()
    email_user_init = Utils.retorna_usuario_autenticado(matricula=matricula).results[0].email
    user = {
        'nome' : params['nome'],
        'orgao' : params['orgao'],
        'telefone' : params['telefone'],
        'cargo' : params['cargo'],
        'setor' : params['setor'],
        'email' : params['email'],
        'matricula' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].matricula,
        'permissao' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].permissao,
        'senha' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
        'favoritos' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].favoritos,
        'itens' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].itens
    }
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(user)
    edit = user_obj.edit_user(id, doc)
    if(email_user_init != email_user_new):
        headers = forget(request)
        response = Response()
        response = HTTPFound(location = request.route_url('login'),
                         headers = headers)
        return response
    else:
        return Response(edit)

@view_config(route_name='edit_password_user', renderer='templates/alterar_senha.pt', permission="gest")
def edit_password_user(request):
    matricula = request.matchdict['matricula']
    user_obj = Utils.create_user_obj()
    search = user_obj.search_user(matricula)
    email = search.results[0].email
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    if (usuario_autenticado.results[0].email ==  email):
        return {
            'nome' : search.results[0].nome,
            'matricula' : search.results[0].matricula,
            'email' : search.results[0].email,
            'orgao' : search.results[0].orgao,
            'telefone' : search.results[0].telefone,
            'cargo' : search.results[0].cargo,
            'setor' : search.results[0].setor,
            'permissao' : search.results[0].permissao,
            'senha' : search.results[0].senha,
            'itens' : search.results[0].itens,
            'favoritos' : search.results[0].favoritos,
            'usuario_autenticado':usuario_autenticado,
        }
    else:
        return HTTPFound(location = request.route_url('home'))

@view_config(route_name='put_password_user', permission="gest")
def put_password_user(request):
    """
    Edita um doc de user apartir do id
    """
    params = request.params
    matricula = params['url']
    email_user = params['email']
    user_obj = Utils.create_user_obj()
    user = {
        'nome' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].nome,
        'orgao' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].orgao,
        'telefone' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].telefone,
        'cargo' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].cargo,
        'setor' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].setor,
        'matricula' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].matricula,
        'email' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].email,
        'permissao' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].permissao,
        'senha' : Utils.hash_password(params['senha']),
        'favoritos' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].favoritos,
        'itens' : Utils.retorna_usuario_autenticado(matricula=matricula).results[0].itens
    }
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(user)
    edit = user_obj.edit_user(id, doc)
    return Response(edit)

@view_config(route_name='init_config_user', renderer='templates/init_config_user.pt')
def init_config_user(request):
    user_obj = Utils.create_user_obj()
    search = user_obj.search_list_users()
    result_count = search.result_count
    if(result_count > 0):
        return HTTPFound(location = request.route_url('login'))
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
    return {'usuario_autenticado':usuario_autenticado}

# Autenticação
@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    user_obj = Utils.create_user_obj()
    search = user_obj.search_list_users()
    result_count = search.result_count
    if(result_count == 0):
        return HTTPFound(location = request.route_url('init_config_user'))
    elif(request.authenticated_userid):
        return HTTPFound(location = request.route_url('home'))
    else:
        user_obj = User(
            nome = 'asdasd',
            matricula = 'asdasd',
            email = 'asdsad',
            orgao = 'asdsad',
            telefone = 'sdasd',
            cargo = 'asdasdasd',
            setor = 'asdasd',
            permissao = 'asdasd',
            senha = 'sadasdasd',
            favoritos = ['asdasdasdasd']
        )
        login_url = request.route_url('login')
        referrer = request.url
        message = 'Você não tem permissão para isso. Autentique-se.'
        if referrer == login_url:
            referrer = request.route_url('root') + 'home' # never use the login form itself as came_from
            message = ''
        came_from = request.params.get('came_from', referrer)
        email = ''
        senha = ''
        is_visible = 'none'
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)
        if 'form.submitted' in request.params:
            email = request.params['email']
            senha = request.params['senha']
            senha_hash = Utils.hash_password(senha)
            try:
                usuario = user_obj.search_user_by_email(email)
                if usuario.results[0].senha == senha_hash:
                    response = Response()
                    headers = remember(request, email)
                    response = HTTPFound(location = came_from,
                                     headers = headers)
                    return response
                message = 'E-mail ou senha incorretos'
            except:
                message = 'E-mail ou senha incorretos'

        if message != '':
            is_visible = "block"
        return dict(
            message = message,
            url = request.application_url + '/login',
            came_from = came_from,
            email = email,
            senha = senha,
            is_visible = is_visible,
            usuario_autenticado = usuario_autenticado,
            )

@view_config(route_name='logout', permission="user")
def logout(request):
    headers = forget(request)
    response = Response()
    response = HTTPFound(location = request.route_url('login'),
                     headers = headers)
    return response

# Coleta
@view_config(route_name='cadastro_coleta', renderer='templates/cadastro_coleta.pt', permission="gest")
def cadastro_coleta(request):
    orgao_obj = Orgao(
        nome = 'teste',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    usuario_autenticado = Utils.retorna_usuario_autenticado(email=request.authenticated_userid)

    return {'orgao_doc': search.results,
            'usuario_autenticado':usuario_autenticado
            }


@view_config(route_name='post_coleta_manual', permission="gest")
def post_coleta_manual(request):
    """
    Post doc ColetaManual
    """
    document = json.loads(request.params['documento'])
    nm_base = document['orgao']
    data_coleta = document['data_coleta']
    softwarelist = document['softwarelist']
    win32_processor_manufacturer = document['win32_processor_manufacturer']
    win32_processor_numberoflogicalprocessors = document['win32_processor_numberoflogicalprocessors']
    win32_processor_caption = document['win32_processor_caption']
    operatingsystem_version = document['operatingsystem_version']
    operatingsystem_installdate = document['operatingsystem_installdate']
    operatingsystem_caption = document['operatingsystem_caption']
    win32_bios_manufacturer = document['win32_bios_manufacturer']

    nm_base_formatted = Utils.format_name(nm_base)
    coleta_dict= {
        "data_coleta": data_coleta,
        "win32_processor": {
            "win32_processor_manufacturer": win32_processor_manufacturer,
            "win32_processor_numberoflogicalprocessors": win32_processor_numberoflogicalprocessors,
            "win32_processor_caption": win32_processor_caption
        },
        "operatingsystem": {
            "operatingsystem_version": operatingsystem_version,
            "operatingsystem_installdate": operatingsystem_installdate,
            "operatingsystem_caption": operatingsystem_caption
        },
        "softwarelist":softwarelist,
        "win32_bios": {
            "win32_bios_manufacturer": win32_bios_manufacturer
        }
    }
    dumps = json.dumps(coleta_dict)
    id_doc = Reports(nm_base_formatted,response_object=False).create_coleta(dumps)
    return Response(str(id_doc))
