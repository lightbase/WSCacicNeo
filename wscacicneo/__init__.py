from pyramid.config import Configurator



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('master', 'master')

    config.add_route('home', 'home')
    config.add_route('graficop', 'graficop')
    config.add_route('notifications', 'notifications')
    config.add_route('admin', 'admin')
    config.add_route('proc', 'proc')
    config.add_route('sistema', 'sistema')
    #Órgão
    config.add_route('orgao', 'orgao')
    config.add_route('post_orgao', 'post_orgao')
    #
    config.add_route('list', 'list')
    config.add_route('gestao', 'gestao')
    config.add_route('bot', 'bot')
    config.add_route('memoria', 'memoria')
    config.add_route('basico', 'basico')
    config.add_route('rede', 'rede')
    config.add_route('escritorio', 'escritorio')
    config.add_route('hd', 'hd')
    config.add_route('config', 'config')
    config.add_route('users', 'users')
    config.add_route('login', 'login')
    config.add_route('reports', 'reports')
    config.add_route('computador', 'computador')
    config.add_route('busca', 'busca')
    config.add_route('gestor', 'gestor')
    config.add_route('diagnostic', 'diagnostic')
    config.add_route('cadastro', 'cadastro')
    config.add_route('sobre', 'sobre')
    config.add_route('perfil', 'perfil')
    config.add_route('configapi','configapi')
    config.add_route('editarorgao','editarorgao')
    config.add_route('notify','notify')
    config.add_route('processador','processador')
    config.add_route('configcoleta','configcoleta')
    config.add_route('configfav','configfav')
    config.add_route('reportsgestor','reportsgestor')
    config.add_route('questionarcoleta','questionarcoleta')
    config.add_route('confighome','confighome')
    config.add_route('db','db')
    config.scan()
    return config.make_wsgi_app()


