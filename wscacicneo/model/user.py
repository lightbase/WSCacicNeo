#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

from requests.exceptions import HTTPError
from wscacicneo import config
import logging
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()


class UserBase():
    """
    Classe para a base de usuários
    """
    def __init__(self, rest_url=None):
        """
        Método construtor
        """
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=False)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)

    @property
    def lbbase(self):
        """
        LB Base de Users
        """
        nome = Field(**dict(
            name='nome',
            description='Nome do Usuário',
            alias='nome',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        matricula = Field(**dict(
            name='matricula',
            alias='matricula',
            description='Matricula do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        email = Field(**dict(
            name='email',
            alias='email',
            description='E-mail do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        telefone = Field(**dict(
            name='telefone',
            alias='telefone',
            description='Telefone do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        orgao = Field(**dict(
            name='orgao',
            alias='orgao',
            description='Orgão do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))


        cargo = Field(**dict(
            name='cargo',
            alias='cargo',
            description='Cargo do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        setor = Field(**dict(
            name='setor',
            alias='setor',
            description='Setor do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        permissao = Field(**dict(
            name='permissao',
            alias='permissao',
            description='Permissão do Usuário',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        
        senha = Field(**dict(
                    name='senha',
                    alias='senha',
                    description='Senha do Usuário',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=False,
                    required=True
        ))
        favoritos = Field(**dict(
                    name='favoritos',
                    alias='favoritos',
                    description='Favoritos do Usuário',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=True,
                    required=False
        ))
        home = Field(**dict(
                    name='home',
                    alias='home',
                    description='Home do Usuário',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=True,
                    required=False
        ))
        itens = Field(**dict(
                    name='itens',
                    alias='itens',
                    description='Itens do Usuário',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=True,
                    required=False
        ))

        url_hash = Field(**dict(
                    name='url_hash',
                    alias='url_hash',
                    description='hash que sera usado para para criar a url',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=True,
                    required=False
        ))

        nm_user = Field(**dict(
                    name='nm_user',
                    alias='nm_user',
                    description='Nome do usuario',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=True,
                    required=False
        ))

        HashUrl_content = Content()
        HashUrl_content.append(nm_user)
        HashUrl_content.append(url_hash)

        HashUrl_metadata = GroupMetadata(
            name='HashUrl',
            alias='HashUrl',
            description='HashUrl',
            multivalued=False
        )

        HashUrl = Group(
            metadata = HashUrl_metadata,
            content = HashUrl_content
        )

        base_metadata = BaseMetadata(
            name='users',
        )

        content_list = Content()
        content_list.append(nome)
        content_list.append(matricula)
        content_list.append(email)
        content_list.append(telefone)
        content_list.append(orgao)
        content_list.append(cargo)
        content_list.append(setor)
        content_list.append(permissao)
        content_list.append(senha)
        content_list.append(favoritos)
        content_list.append(home)
        content_list.append(itens)
        content_list.append(HashUrl)

        lbbase = Base(
            metadata=base_metadata,
            content=content_list
        )

        return lbbase

    @property
    def metaclass(self):
        """
        Retorna metaclass para essa base
        """
        return self.lbbase.metaclass()
    
    def create_base(self):
        """
        Cria base no LB
        """
        try:
            response = self.baserest.create(self.lbbase)
            return True
        except HTTPError:
            raise IOError('Error inserting base in LB')

    def remove_base(self):
        """
        Remove base from Lightbase
        :param lbbase: LBBase object instance
        :return: True or Error if base was not excluded
        """
        try:
            response = self.baserest.delete(self.lbbase)
            return True
        except HTTPError:
            raise IOError('Error excluding base from LB')

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            response = self.baserest.get(self.lbbase.metadata.name)
            return True
        except HTTPError:
            return False


user_base = UserBase()


class User(user_base.metaclass):
    """
    Classe genérica de usuários
    """
    def __init__(self, **args):
        super(User, self).__init__(**args)
        self.documentrest = user_base.documentrest
        valid_users = [
            "Administrador",
            "Gestor"
        ]

    @property
    def permissao(self):
        """
        Getter da permissão
        """
        return user_base.metaclass.permissao.__get__(self)

    @permissao.setter
    def permissao(self, value):
        valid_users = [
            "Administrador",
            "Gestor"
        ]
        if value not in valid_users:
            raise AttributeError("Permissão de usuário inválida")

        user_base.metaclass.permissao.__set__(self, value)

    def user_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(user_base.lbbase, self)

    def user_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(user_base.lbbase, self)

    def create_user(self):
        """
        Insert document on base

        :return: Document creation ID
        """

        document = self.user_to_json()
        try:
            result = user_base.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result

    def search_user(self, matricula):
        """
        Busca registro completo do usuário pela matricula
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'matricula' = '"+matricula+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def search_list_users(self):
        """
        Retorna todos os docs da base
        """
        search = Search(
            limit=None
        )
        results = self.documentrest.get_collection(search)

        return results

    def create_favoritos(self, id, path, value):
        """
        altera um doc ou path do doc
        """
        results = self.documentrest.create_path(id, path, value)

        return results

    def edit_user(self, id, doc):
        """
        altera um doc ou path do doc
        """
        results = self.documentrest.update(id, doc)

        return results

    def get_user_by_id(self, id_user):
        """
        Retorna um documento a partir do id
        """

        results = self.documentrest.get(id_user)

        return results

    def delete_user(self, id):
        """
        Deleta o Órgao apartir do ID
        """
        results = user_base.documentrest.delete(id)

        return results

    def remove_path(self, id, path):
        """
        Deleta um valor especifico de um campo multivalorado
        """
        results = self.documentrest.delete_path(id, path)

        return results

    def search_user_by_email(self, email):
        """
        Busca registro completo do usuário pelo email
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'email' = '"+email+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def add_home_report(self, report_name, userid):
        search = Search(
            literal="document->>'email' = '"+userid+"'"
        )
        path_list=[
            {
              "path": "home",
              "mode": "insert",
              "fn": None,
              "args": [report_name]
            }
        ]
        results = self.documentrest.update_collection(
            search_obj=search, path_list=path_list)

    def edit_home_report(self, report_name, userid):
        search = Search(
            literal="document->>'email' = '"+userid+"'"
        )
        path_list=[
            {
              "path": "home",
              "mode": "update",
              "fn": None,
              "args": [report_name]
            }
        ]
        results = self.documentrest.update_collection(
            search_obj=search, path_list=path_list)



