import requests
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from .models import (
    DBSession,
    SistemaOperacional,
    )

engine = create_engine('postgresql://rest:rest@localhost/cacic')
REST_URL = 'http://api.brlight.net/api'

Session = sessionmaker(bind=engine)
session = Session()
@view_config(route_name='master', renderer='templates/master.pt')
def master(request):
    url = REST_URL + '/orgao_sg/doc'
    json_reg = request.params
    data = {'value': json_reg}
    response = requests.post(url, data=data)
    return response.text

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


@view_config(route_name='busca', renderer='templates/busca.pt')
def my_view8(request):
    query = session.query(SistemaOperacional).all()
    data = dict()
    #data = {'items': []}
    data["items"] = list()
    wc = 0
    uc = 0
    dc = 0
    for q in query:
        w = q.te_desc_so.count("Windows")
        u = q.te_desc_so.count("Ubuntu")
        d = q.te_desc_so.count("Debian")
        wc += w
        uc += u
        dc += d
        #d = {'id_so': 'valor'}
    d = dict(
        wcount = str(wc),
        ucount = str(uc),
        dcount = str(dc),
        a = 'Windows',
        b = 'Ubuntu',
        c = 'Debian'
        )
    data["items"].append(d)
    #print (wc)
    #print (uc)
    #print (dc)

    return {'project':'WSCacicNeo', 'data': data}
