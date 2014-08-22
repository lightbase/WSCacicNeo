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

@view_config(route_name='editarorgao', renderer='templates/editarorgao.pt')
def editarorgao(request):
    return {'project': 'WSCacicNeo'}

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

@view_config(route_name='delete_orgao')
def delete_orgao(request):
    doc = request.params
    nm_orgao = doc['nome']
    orgao_obj = Orgao(
        nome = doc['nome'],
        cargo = doc['gestor'],
        coleta = doc['coleta'],
        sigla = doc['sigla'],
        endereco = doc['end'],
        email = doc['email'],
        telefone = doc['telefone']
    )
    search = orgao_obj.search_orgao(nm_orgao)
    id = search.results[0]._metadata.id_doc
    delete = orgao_obj.delete_orgao(id)

    return Response(str(delete))

