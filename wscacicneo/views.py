from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from .models import (
    DBSession,
    SistemaOperacional,
    )

engine = create_engine('postgresql://rest:rest@localhost/cacic')

Session = sessionmaker(bind=engine)
session = Session()
@view_config(route_name='master', renderer='templates/master.pt')
def master(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='reports', renderer='templates/reports.pt')
def reports(request):
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

@view_config(route_name='sobre', renderer='templates/sobre.pt')
def sobre(request):
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

# @view_config(route_name='estatisticas', renderer='templates/estatisticas.pt')
# def estatisticas(request):
#     response = requests.get('%s/base?$$={"select":"*"}' %(rest_url)).json()
#     results = response['results']

#     return {'project': 'WSCacicNeo', 'results': json.dumps(results)}

# @view_config(route_name='downloads', renderer='templates/downloads.pt')
# def downloads(request):
#     return {'project': 'WSCacicNeo'}

# @view_config(route_name='relatorios', renderer='templates/relatorios.pt')
# def relatorios(request):
#     response = requests.get('http://api.brlight.org/reg/WMI/3').json()
#     #response = requests.get('http://api.brlight.org/base/5').json()

#     return {'project': 'WSCacicNeo', 'reg': response}

# @view_config(route_name='mensagens', renderer='templates/mensagens.pt')
# def mensagens(request):
#     return {'project': 'WSCacicNeo'}

# @view_config(route_name='ajuda', renderer='templates/ajuda.pt')
# def ajuda(request):
#     return {'project': 'WSCacicNeo'}

# @view_config(route_name='usuario', renderer='templates/usuario.pt')
# def usuario(request):
#     return {'project': 'WSCacicNeo'}

# @view_config(route_name='ferramentas', renderer='templates/ferramentas.pt')
# def ferramentas(request):
#     return {'project': 'WSCacicNeo'}

# @view_config(route_name='login', renderer='templates/login.pt')
# def login(request):
#     return {'project': 'WSCacicNeo'}
