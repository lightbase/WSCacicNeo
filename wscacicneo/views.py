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
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from liblightbase.lbrest.document import DocumentREST


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

@view_config(route_name='notifications', renderer='templates/dashboard.pt')
def notifications(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='admin', renderer='templates/admin.pt')
def admin(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='diagnostic', renderer='templates/diagnostic.pt')
def diagnostic(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='users', renderer='templates/users.pt')
def users(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='cadastro', renderer='templates/cadastro.pt')
def cadastro(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
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
        telefone = '(61) 2025-4117'
    )
    search = orgao_obj.search_list_orgaos()
    return {'orgao_doc': search.results}

@view_config(route_name='config', renderer='templates/config.pt')
def config(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='list', renderer='templates/list.pt')
def list(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='sobre', renderer='templates/sobre.pt')
def sobre(request):
    return {'project': 'WSCacicNeo'}

#formularios de cadastro de coleta

@view_config(route_name='computador', renderer='templates/computador.pt')
def computador(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='processador', renderer='templates/processador.pt')
def proc(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='memoria', renderer='templates/memoria.pt')
def memoria(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='hd', renderer='templates/hd.pt')
def hd(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='escritorio', renderer='templates/escritorio.pt')
def escritorio(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='rede', renderer='templates/rede.pt')
def rede(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='basico', renderer='templates/basico.pt')
def basico(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='sistema', renderer='templates/sistema.pt')
def sistema(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='bot', renderer='templates/bot.pt')
def bot(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='configapi', renderer='templates/configapi.pt')
def configapi(request):
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
        telefone = '(61) 2025-4117'
    )
    search = orgao_obj.search_orgao(sigla)
    return {
        'nome' : search.results[0].nome,
        'cargo' : search.results[0].cargo,
        'coleta' : search.results[0].coleta,
        'sigla' : search.results[0].sigla,
        'endereco' : search.results[0].endereco,
        'email' : search.results[0].email,
        'telefone' : search.results[0].telefone
    }

@view_config(route_name='notify', renderer='templates/notify.pt')
def notify(request):
    return {'project': 'WSCacicNeo'}

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
        telefone = doc['telefone']
    )

    id_doc = orgao_obj.create_orgao()
    print(id_doc)

    return Response(str(id_doc))

@view_config(route_name='put_orgao')
def put_orgao(request):
    """
    Edita um doc apartir do id
    """
    doc = request.params
    nm_orgao = doc['url']
    orgao_obj = Orgao(
        nome = doc['nome'],
        cargo = doc['gestor'],
        coleta = doc['coleta'],
        sigla = doc['sigla'],
        endereco = doc['end'],
        email = doc['email'],
        telefone = doc['telefone']
    )
    search = orgao_obj.search_orgao(sigla)
    id = search.results[0]._metadata.id_doc
    edit = Orgao.edit_orgao(id, doc)

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
        telefone = 'sadasd'
    )
    search = orgao_obj.search_orgao(sigla)
    id = search.results[0]._metadata.id_doc
    delete = orgao_obj.delete_orgao(id)

    return Response(delete)

#URL Users

@view_config(route_name='post_user')
def post_user(request):
    """
    Post doc users
    """
    rest_url = REST_URL
    userbase = UserBase().lbbase
    doc = request.params
    user_obj = User(
        nome = doc['nome'],
        matricula = doc['matricula'],
        email = doc['email'],
        orgao = doc['orgao'],
        telefone = doc['telefone'],
        cargo = doc['cargo'],
        setor = doc['setor'],
        permissao = doc['permissao']
    )

    id_doc = user_obj.create_user()
    print(id_doc)

    return Response(str(id_doc))
