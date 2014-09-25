import requests
import json
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from .models import (
    DBSession,
    SistemaOperacional,
    )
from wscacicneo.utils.utils import Utils
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from liblightbase.lbrest.document import DocumentREST
from pyramid.view import forbidden_view_config

from pyramid.security import (
    remember,
    forget,
    )

engine = create_engine('postgresql://rest:rest@localhost/cacic')
REST_URL = 'http://api.brlight.net/api'

Session = sessionmaker(bind=engine)
session = Session()

@view_config(route_name='blankmaster', renderer='templates/blankmaster.pt')
def blankmaster(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='master', renderer='templates/master.pt')
def master(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='root')
def root(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='reports', renderer='templates/reports.pt')
def reports(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='gestao', renderer='templates/gestao.pt')
def gestao(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='perfil', renderer='templates/perfil.pt')
def perfil(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='graficop', renderer='templates/graficop.pt')
def graficop(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='gestor', renderer='templates/gestor.pt')
def gestor(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='notify', renderer='templates/notify_coleta.pt')
def notify(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='admin', renderer='templates/admin.pt')
def admin(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='diagnostic', renderer='templates/diagnostic.pt')
def diagnostic(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='cadastro', renderer='templates/cadastro.pt')
def cadastro(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='orgao', renderer='templates/orgao.pt')
def orgao(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='listorgao', renderer='templates/list_orgao.pt')
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
    return {'orgao_doc': search.results}

@view_config(route_name='favoritos', renderer='templates/favoritos.pt')
def favoritos(request):
    matricula = request.matchdict['matricula']
    user_obj = User(
        nome = 'base',
        matricula = matricula,
        email = 'base@gov.br',
        orgao = 'orgao',
        telefone = 'telefone',
        cargo = 'cargo',
        setor = 'setor',
        permissao = 'Gestor',
        favoritos = ['asdsadasd', 'asdasdasd'],
        senha = 'senha'
    )
    search = user_obj.search_user(matricula)
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
        'senha' : search.results[0].senha
    }

@view_config(route_name='config', renderer='templates/config.pt')
def config(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='list', renderer='templates/list.pt')
def list(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='sobre', renderer='templates/sobre.pt')
def sobre(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='base_de_dados', renderer='templates/base_dados.pt')
def base_de_dados(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='editorgao', renderer='templates/editarorgao.pt')
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
    return {
        'nome' : search.results[0].nome,
        'cargo' : search.results[0].cargo,
        'coleta' : search.results[0].coleta,
        'sigla' : search.results[0].sigla,
        'endereco' : search.results[0].endereco,
        'email' : search.results[0].email,
        'telefone' : search.results[0].telefone,
        'url' : search.results[0].url
    }

@view_config(route_name='configcoleta', renderer='templates/configcoleta.pt')
def configcoleta(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='configfav', renderer='templates/configfav.pt')
def configfav(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='reportsgestor', renderer='templates/reportsgestor.pt')
def reportsgestor(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='questionarcoleta', renderer='templates/questionarcoleta.pt')
def questionarcoleta(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='confighome', renderer='templates/confighome.pt')
def confighome(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='db', renderer='templates/db.pt')
def db(request):
    return {'project': 'WSCacicNeo'}

#URL Órgaos

@view_config(route_name='post_orgao')
def post_orgao(request):
    """
    Post doc órgãos
    """
    rest_url = REST_URL
    orgaobase = OrgaoBase().lbbase
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

@view_config(route_name='put_orgao')
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

@view_config(route_name='delete_orgao')
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

    return Response(delete)

#URL Users

@view_config(route_name='user', renderer='templates/user.pt', permission='edit')
def user(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='post_user')
def post_user(request):
    """
    Post doc users
    """
    rest_url = REST_URL
    userbase = UserBase().lbbase
    doc = request.params
    email_user = doc['email']
    email_is_institucional = Utils.verifica_email_institucional(email_user)
    if(email_is_institucional):
        document = doc['favoritos']
        favoritos = [document]
        itens = [doc['lista_orgao'], doc['cadastro_orgao'], doc['lista_user'], doc['cadastro_user'], doc['coleta'], doc['notify']]
        user_obj = User(
            nome = doc['nome'],
            matricula = doc['matricula'],
            email = doc['email'],
            orgao = doc['orgao'],
            telefone = doc['telefone'],
            cargo = doc['cargo'],
            setor = doc['setor'],
            permissao = doc['permissao'],
            senha = doc['senha'],
            favoritos = favoritos,
            itens = itens
        )
        id_doc = user_obj.create_user()

        return Response(str(id_doc))
    else:
        return {"yololo":"yololo"}

@view_config(route_name='edituser', renderer='templates/editaruser.pt', permission="edit")
def edituser(request):
    matricula = request.matchdict['matricula']
    user_obj = User(
        nome = 'base',
        matricula = matricula,
        email = 'base@gov.br',
        orgao = 'orgao',
        telefone = 'telefone',
        cargo = 'cargo',
        setor = 'setor',
        permissao = 'Gestor',
        senha = 'senha'
    )
    search = user_obj.search_user(matricula)
    return {
        'nome' : search.results[0].nome,
        'matricula' : search.results[0].matricula,
        'email' : search.results[0].email,
        'orgao' : search.results[0].orgao,
        'telefone' : search.results[0].telefone,
        'cargo' : search.results[0].cargo,
        'setor' : search.results[0].setor,
        'permissao' : search.results[0].permissao,
        'senha' : search.results[0].senha
    }

@view_config(route_name='post_notify')
def post_notify(request):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    return { }

@view_config(route_name='put_user')
def put_user(request):
    """
    Edita um doc de user apartir do id
    """
    params = request.params
    matricula = params['url']
    user_obj = User(
        nome = params['nome'],
        matricula = params['matricula'],
        email = params['email'],
        orgao = params['orgao'],
        telefone = params['telefone'],
        cargo = params['cargo'],
        setor = params['setor'],
        permissao = params['permissao'],
        senha = params['senha']
    )
    user = {
        'nome' : params['nome'],
        'matricula' : params['matricula'],
        'email' : params['email'],
        'orgao' : params['orgao'],
        'telefone' : params['telefone'],
        'cargo' : params['cargo'],
        'setor' : params['setor'],
        'permissao' : params['permissao'],
        'senha' : params['senha']
    }
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(user)
    edit = user_obj.edit_user(id, doc)

    return Response(edit)

@view_config(route_name='listuser', renderer='templates/list_user.pt', permission="view")
def listuser(request):
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
    search = user_obj.search_list_users()
    return {'user_doc': search.results}

@view_config(route_name='delete_user')
def delete_user(request):
    """
    Deleta doc apartir do id
    """
    doc = request.params
    matricula = request.matchdict['matricula']
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
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    delete = user_obj.delete_user(id)
    return Response(delete)

@view_config(route_name='edit_favoritos')
def edit_favoritos(request):
    """
    Editar do Favoritos
    """
    documento = json.loads(request.params['documento'])
    matricula = documento['matricola']
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

    return Response(edit)

@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
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
    if referrer == login_url:
        referrer = request.route_url('root') + 'home' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    email = ''
    senha = ''
    if 'form.submitted' in request.params:
        email = request.params['email']
        senha = request.params['senha']
        usuario = user_obj.search_user_by_email(email)
        if usuario.results[0].senha == senha:
            headers = remember(request, email)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        email = email,
        senha = senha,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('login'),
                     headers = headers)


