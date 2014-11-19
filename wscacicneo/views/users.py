#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
from pyramid.view import view_config
from wscacicneo.utils.utils import Utils
from wscacicneo.model.notify import Notify
from pyramid.httpexceptions import HTTPFound
from wscacicneo.model.orgao import Orgao
from pyramid.response import Response
from wscacicneo.model.user import User
from wscacicneo.model import base_reports
from wscacicneo.model.reports import Reports
from wscacicneo.model import config_reports
from wscacicneo.model import user as model_usuario
from pyramid.security import (
    remember,
    forget,
    )

REST_URL = 'http://api.brlight.net/api'


class Users(object):
    """
    Métodos básicos do sistema
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request

    # Lista de Notificação
    @view_config(route_name='list_notify', renderer='templates/list_notify.pt', permission="gest")
    def list_notify(self):
        notify_obj = Notify(
            orgao = 'deasdsd',
            data_coleta = 'saudhasd',
            notify = 'sadsad',
            coment = 'sadasd',
            status = 'sadasd'
        )
        reg = notify_obj.search_list_notify()
        doc = reg.results
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {
            'doc': doc,
            'usuario_autenticado':usuario_autenticado
        }

    @view_config(route_name='delete_notify', permission="gest")
    def delete_notify(self):
        orgao = self.request.matchdict['orgao']
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
        return HTTPFound(location = self.request.route_url('list_notify'))

    @view_config(route_name='edit_notify', permission="gest")
    def edit_notify(self):
        orgao = self.request.matchdict['orgao']
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
        return HTTPFound(location = self.request.route_url('list_notify'))


    @view_config(route_name='notify', renderer='templates/notify_coleta.pt', permission="gest")
    def notify(self):
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
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)

        return {'orgao_doc': search.results,
                'usuario_autenticado':usuario_autenticado
                }

    @view_config(route_name='post_notify', permission="gest")
    def post_notify(self):
        requests = self.request.params
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
    def orgao(self):
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {'usuario_autenticado':usuario_autenticado}

    # Views de Favoritos
    @view_config(route_name='favoritos', renderer='templates/favoritos.pt', permission="gest")
    def favoritos(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        if (usuario_autenticado.results[0].email ==  email):
            search = user_obj.search_user(matricula)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
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
            return HTTPFound(location = self.request.route_url('home'))

    @view_config(route_name='edit_favoritos', permission="gest")
    def edit_favoritos(self):
        """
        Editar do Favoritos
        """
        documento = json.loads(self.request.params['documento'])
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
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return Response(edit)

    @view_config(route_name='conf_report', renderer='templates/conf_report.pt')
    def conf_report(self):
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
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)

        return {'orgao_doc': search.results,
                'usuario_autenticado':usuario_autenticado
                }

    @view_config(route_name='report_itens', renderer='templates/report.pt', permission="user")
    def report_itens(self):
        orgao_nm = self.request.matchdict['nm_orgao']
        nm_orgao = Utils.format_name(orgao_nm)
        report_base = base_reports.ReportsBase(nm_orgao)
        if(report_base.is_created() == False):
            create_base = report_base.create_base()
            attr = self.request.matchdict['attr']
            child = self.request.matchdict['child']
            data = Reports(nm_orgao).count_attribute(attr, child)
            reports_config = config_reports.ConfReports(nm_orgao)
            for items in data:
                data_json = {attr : { attr+'_item' : items, attr+'_amount': str(data[items])}}
                document = json.dumps(data_json)
                reports_config.create_coleta(document)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {'data': data,
                    'status_base': create_base,
                    'usuario_autenticado':usuario_autenticado
                    }
        else:
            orgao_nm = self.request.matchdict['nm_orgao']
            nm_orgao = Utils.format_name(orgao_nm)
            attr = self.request.matchdict['attr']
            child = self.request.matchdict['child']
            data = Reports(nm_orgao).count_attribute(attr, child)
            usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
            return {
                    'data': data,
                    'usuario_autenticado':usuario_autenticado
                    }

    # Users

    @view_config(route_name='user', renderer='templates/user.pt', permission='admin')
    def user(self):
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {'usuario_autenticado':usuario_autenticado}

    @view_config(route_name='post_user', permission="admin")
    def post_user(self):
        """
        Post doc users
        """
        rest_url = REST_URL
        userbase = model_usuario.UserBase().lbbase
        doc = self.request.params
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
    def post_first_user(self):
        """
        Post doc users
        """
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        result_count = search.result_count
        if(result_count == 0):
            rest_url = REST_URL
            userbase = model_usuario.UserBase().lbbase
            doc = self.request.params
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
            return HTTPFound(location = self.request.route_url('home'))

    @view_config(route_name='edituser', renderer='templates/editaruser.pt', permission="admin")
    def edituser(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
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
    def put_user(self):
        """
        Edita um doc de user apartir do id
        """
        params = self.request.params
        matricula = params['url']
        email_user = params['email']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        permissao_usuario_edit = search.results[0].permissao
        email_usuario_edit = search.results[0].email
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
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
                headers = forget(self.request)
                response = Response()
                response = HTTPFound(location = self.request.route_url('login'),
                                 headers = headers)
                return response
        else:
            return {"emailerrado":"E-mail não institucional"}

    @view_config(route_name='listuser', renderer='templates/list_user.pt', permission="admin")
    def listuser(self):
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {'user_doc': search.results,
                'usuario_autenticado':usuario_autenticado
                }

    @view_config(route_name='delete_user', permission="admin")
    def delete_user(self):
        """
        Deleta doc apartir do id
        """
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        doc = self.request.params
        matricula = self.request.matchdict['matricula']
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
    def edit_profile_user(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
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
            return HTTPFound(location = self.request.route_url('home'))

    @view_config(route_name='put_profile_user', permission="gest")
    def put_profile_user(self):
        """
        Edita um doc de user apartir do id
        """
        params = self.request.params
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
            headers = forget(self.request)
            response = Response()
            response = HTTPFound(location = self.request.route_url('login'),
                             headers = headers)
            return response
        else:
            return Response(edit)

    @view_config(route_name='edit_password_user', renderer='templates/alterar_senha.pt', permission="gest")
    def edit_password_user(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
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
            return HTTPFound(location = self.request.route_url('home'))

    @view_config(route_name='put_password_user', permission="gest")
    def put_password_user(self):
        """
        Edita um doc de user apartir do id
        """
        params = self.request.params
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
    def init_config_user(self):
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        result_count = search.result_count
        if(result_count > 0):
            return HTTPFound(location = self.request.route_url('login'))
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        return {'usuario_autenticado':usuario_autenticado}