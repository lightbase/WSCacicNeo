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
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
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
        itens = Field(**dict(
                    name='itens',
                    alias='itens',
                    description='Itens do Usuário',
                    datatype='Text',
                    indices=['Textual'],
                    multivalued=True,
                    required=False
        ))

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
        content_list.append(itens)

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
        response = self.baserest.create(self.lbbase)
        if response.status_code == 200:
            return self.lbbase
        else:
            return None

    def remove_base(self):
        """
        Remove base from Lightbase
        :param lbbase: LBBase object instance
        :return: True or Error if base was not excluded
        """
        response = self.baserest.delete(self.lbbase)
        if response.status_code == 200:
            return True
        else:
            raise IOError('Error excluding base from LB')

user_base = UserBase()

class User(user_base.metaclass):
    """
    Classe genérica de usuários
    """
    def __init__(self, **args):
        super(User, self).__init__(**args)
        self.documentrest = user_base.documentrest

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