#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import datetime
from pyramid.view import view_config
from wscacicneo.utils.utils import Utils
from wscacicneo.model.notify import Notify
from pyramid.httpexceptions import HTTPFound
from wscacicneo.model.orgao import Orgao
from pyramid.response import Response
from wscacicneo.model.user import User
from ..model import atividade
from wscacicneo.model import user as model_usuario
from wscacicneo.search.orgao import SearchOrgao
from wscacicneo.search.user import SearchUser
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
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    # Views de Favoritos
    #@view_config(route_name='favoritos', renderer='../templates/favoritos.pt', permission="gest")
    def favoritos(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        if (self.usuario_autenticado.email ==  email):
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
                'senha' : search.results[0].senha,
                'usuario_autenticado': self.usuario_autenticado
            }
        else:
            return HTTPFound(location=self.request.route_url('home'))

    #@view_config(route_name='edit_favoritos', permission="gest")
    def edit_favoritos(self):
        """
        Editar do Favoritos
        """
        documento = json.loads(self.request.params['documento'])
        matricula = documento['matricula']
        user_obj = SearchUser(matricula).search_by_name()
        user = {
            'nome': documento['nome'],
            'matricula': documento['matricula'],
            'email': documento['email'],
            'orgao': documento['orgao'],
            'telefone': documento['telefone'],
            'cargo': documento['cargo'],
            'setor': documento['setor'],
            'permissao': documento['permissao'],
            'senha': documento['senha'],
            'itens': documento['itens'],
            'favoritos': documento['favoritos']
        }
        search = user_obj.search_user(matricula)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)
        return Response(edit)

    # Users

    #@view_config(route_name='user', renderer='../templates/user.pt', permission='admin')
    def user(self):
        orgao_obj = Utils.create_orgao_obj()
        distinct_orgaos = orgao_obj.get_distinct_orgaos("document->>'nome'")
        return {
            'usuario_autenticado': self.usuario_autenticado,
            'orgaos': distinct_orgaos.results
        }

    #@view_config(route_name='post_user', permission="admin")
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
            at = atividade.Atividade(
                tipo='insert',
                usuario=self.usuario_autenticado.nome,
                descricao='Cadastrou o  Usuario '+ doc['nome'],
                data=datetime.datetime.now()
            )
            at.create_atividade()
            id_doc = user_obj.create_user()
            session = self.request.session
            session.flash('Cadastro realizado com sucesso', queue="success")
            return Response(str(id_doc))
        else:
            return {"emailerrado":"emailerrado"}

    #@view_config(route_name='post_first_user')
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

                at = atividade.Atividade(
                    tipo='insert',
                    usuario='Sistema',
                    descricao='Cadastrou o usuário '+ doc['nome'],
                    data=datetime.datetime. now()
                )
                at.create_atividade()
                session = self.request.session
                session.flash('Usuário cadastrado com sucesso', queue="success")
                return Response(str(id_doc))
            else:
                return {"emailerrado": "emailerrado"}
        else:
            return HTTPFound(location = self.request.route_url('home'))

    #@view_config(route_name='edituser', renderer='../templates/editaruser.pt', permission="admin")
    def edituser(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        orgao_obj = Utils.create_orgao_obj()
        distinct_orgaos = orgao_obj.get_distinct_orgaos("document->>'nome'")
        return {
            'nome': search.results[0].nome,
            'matricula': search.results[0].matricula,
            'email': search.results[0].email,
            'orgao': search.results[0].orgao,
            'telefone': search.results[0].telefone,
            'cargo': search.results[0].cargo,
            'setor': search.results[0].setor,
            'permissao': search.results[0].permissao,
            'senha': search.results[0].senha,
            'itens': search.results[0].itens,
            'favoritos': search.results[0].favoritos,
            'usuario_autenticado': self.usuario_autenticado,
            'orgaos': distinct_orgaos.results
        }

    #@view_config(route_name='put_user', permission="admin")
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
        usuario_autenticado_email = self.usuario_autenticado.email
        edit_yourself = False
        if usuario_autenticado_email == email_usuario_edit:
            edit_yourself = True
            email_user = usuario_autenticado_email
        if params['permissao'] == "Administrador" and params['permissao'] != permissao_usuario_edit:
            itens = [params['lista_orgao'], params['cadastro_orgao'], params['lista_user'], params['cadastro_user'], params['notify']]
            favoritos = [params['favoritos']]
            user = {
                'nome': params['nome'],
                'matricula': params['matricula'],
                'email': params['email'],
                'orgao': params['orgao'],
                'telefone': params['telefone'],
                'cargo': params['cargo'],
                'setor': params['setor'],
                'permissao': params['permissao'],
                'senha': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
                'favoritos': favoritos,
                'itens': itens
            }
        elif params['permissao'] == "Gestor" and params['permissao'] != permissao_usuario_edit:
            itens = [params['notify']]
            favoritos = [params['favoritos']]
            user = {
                'nome': params['nome'],
                'matricula': params['matricula'],
                'email': params['email'],
                'orgao': params['orgao'],
                'telefone': params['telefone'],
                'cargo': params['cargo'],
                'setor': params['setor'],
                'permissao': params['permissao'],
                'senha': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
                'favoritos': favoritos,
                'itens': itens
            }
        else:
            user = {
                'nome': params['nome'],
                'matricula': params['matricula'],
                'email': params['email'],
                'orgao': params['orgao'],
                'telefone': params['telefone'],
                'cargo': params['cargo'],
                'setor': params['setor'],
                'permissao': params['permissao'],
                'senha': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
                'favoritos': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].favoritos,
                'itens': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].itens
            }
        id = search.results[0]._metadata.id_doc
        email_is_institucional = Utils.verifica_email_institucional(email_user)
        at = atividade.Atividade(
            tipo='put',
            usuario=self.usuario_autenticado.nome,
            descricao='Editou o  usuario '+params['nome'],
            data=datetime.datetime.now()
        )
        at.create_atividade()

        session = self.request.session
        if email_is_institucional:
            doc = json.dumps(user)
            edit = user_obj.edit_user(id, doc)
            if edit_yourself == False:
                return Response(edit)
                session.flash('Alteração realizado com sucesso', queue="success")
            else:
                # Remove sessão do usuário
                session.invalidate()
                headers = forget(self.request)
                response = Response()
                session.flash('Alteração realizado com sucesso. Você estará sendo desconectado. Reconecte-se.', queue="success")
                response = HTTPFound(location=self.request.route_url('login'),
                                     headers=headers)
                return response
        else:
            return {"emailerrado": "E-mail não institucional"}

    #@view_config(route_name='listuser', renderer='../templates/list_user.pt', permission="admin")
    def listuser(self):
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        return {'user_doc': search.results,
                'usuario_autenticado': self.usuario_autenticado
                }

    #@view_config(route_name='delete_user', permission="admin")
    def delete_user(self):
        """
        Deleta doc apartir do id
        """
        doc = self.request.params
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        nome = search.results[0].nome
        at = atividade.Atividade(
            tipo='delete',
            usuario=self.usuario_autenticado.nome,
            descricao='Deletou o usuario '+nome,
            data=datetime.datetime.now()
        )
        at.create_atividade()
        session = self.request.session
        if self.usuario_autenticado.email != email:
            id = search.results[0]._metadata.id_doc
            delete = user_obj.delete_user(id)
            if delete:
                session.flash('Usuário apagado com sucesso', queue="success")
            else:
                session.flash('Erro ao apagar o usuário', queue="error")
            return HTTPFound(location=self.request.route_url('listuser'))
        else:
            session.flash('Você não pode apagar a si mesmo.', queue="error")
            return HTTPFound(location=self.request.route_url('listuser'))

    #@view_config(route_name='edit_profile_user', renderer='../templates/editarperfil.pt', permission="gest")
    def edit_profile_user(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        orgao_obj = Utils.create_orgao_obj()
        distinct_orgaos = orgao_obj.get_distinct_orgaos("document->>'nome'")
        if self.usuario_autenticado.email == email:
            return {
                'nome': search.results[0].nome,
                'matricula': search.results[0].matricula,
                'email': search.results[0].email,
                'orgao': search.results[0].orgao,
                'telefone': search.results[0].telefone,
                'cargo': search.results[0].cargo,
                'setor': search.results[0].setor,
                'permissao': search.results[0].permissao,
                'senha': search.results[0].senha,
                'itens': search.results[0].itens,
                'favoritos': search.results[0].favoritos,
                'usuario_autenticado': self.usuario_autenticado,
                'orgaos': distinct_orgaos.results
            }
        else:
            return HTTPFound(location = self.request.route_url('home'))

    #@view_config(route_name='put_profile_user', permission="gest")
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
            'nome': params['nome'],
            'orgao': params['orgao'],
            'telefone': params['telefone'],
            'cargo': params['cargo'],
            'setor': params['setor'],
            'email': params['email'],
            'matricula': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].matricula,
            'permissao': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].permissao,
            'senha': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].senha,
            'favoritos': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].favoritos,
            'itens': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].itens
        }
        search = user_obj.search_user(matricula)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)
        session = self.request.session
        if email_user_init != email_user_new:
            session.invalidate()
            headers = forget(self.request)
            response = Response()
            response = HTTPFound(location=self.request.route_url('login'))
                                 #,headers=headers)
            session.flash('Alteração realizado com sucesso. Você está sendo desconectado. Reconecte-se.', queue="success")
            return response
        else:
            session.flash('Alteração realizado com sucesso.', queue="success")
            return Response(edit)

    #@view_config(route_name='edit_password_user', renderer='../templates/alterar_senha.pt', permission="gest")
    def edit_password_user(self):
        matricula = self.request.matchdict['matricula']
        user_obj = Utils.create_user_obj()
        search = user_obj.search_user(matricula)
        email = search.results[0].email
        if self.usuario_autenticado.email ==  email:
            return {
                'nome': search.results[0].nome,
                'matricula': search.results[0].matricula,
                'email': search.results[0].email,
                'orgao': search.results[0].orgao,
                'telefone': search.results[0].telefone,
                'cargo': search.results[0].cargo,
                'setor': search.results[0].setor,
                'permissao': search.results[0].permissao,
                'senha': search.results[0].senha,
                'itens': search.results[0].itens,
                'favoritos': search.results[0].favoritos,
                'usuario_autenticado': self.usuario_autenticado,
            }
        else:
            return HTTPFound(location=self.request.route_url('home'))

    #@view_config(route_name='put_password_user', permission="gest")
    def put_password_user(self):
        """
        Edita um doc de user apartir do id
        """
        params = self.request.params
        matricula = params['url']
        email_user = params['email']
        user_obj = Utils.create_user_obj()
        user = {
            'nome': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].nome,
            'orgao': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].orgao,
            'telefone': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].telefone,
            'cargo': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].cargo,
            'setor': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].setor,
            'matricula': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].matricula,
            'email': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].email,
            'permissao': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].permissao,
            'senha': Utils.hash_password(params['senha']),
            'favoritos': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].favoritos,
            'itens': Utils.retorna_usuario_autenticado(matricula=matricula).results[0].itens
        }
        search = user_obj.search_user(matricula)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)
        session = self.request.session
        session.flash('Alteração realizado com sucesso', queue="success")
        return Response(edit)

    #@view_config (route_name='init_config_user', renderer='../templates/init_config_user.pt')
    def init_config_user(self):
        if Utils.check_has_user():
            return HTTPFound(location = self.request.route_url('login'))
        orgao_obj = Utils.create_orgao_obj()
        distinct_orgaos = orgao_obj.get_distinct_orgaos("document->>'nome'")
        return {
            'usuario_autenticado': self.usuario_autenticado,
            'orgaos': distinct_orgaos.results
        }

    def add_user_home_report(self):
        user_obj = Utils.create_user_obj()
        report_name = self.request.params['report_name']
        user_obj.add_home_report(report_name, self.usuario_autenticado.email)
        return Response('OK')
