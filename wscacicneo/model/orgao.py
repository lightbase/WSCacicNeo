#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

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

class OrgaoBase():
    """
    Classe para a base de órgãos
    """
    def __init__(self, rest_url=None):
        """
        Método construtor
        """
        if rest_url is None:
            self.rest_url= config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)

    @property
    def lbbase(self):
        """
        LB Base do órgão
        """
        nome = Field(**dict(
            name='nome',
            description='Nome do órgão',
            alias='nome',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        sigla = Field(**dict(
            name='sigla',
            alias='sigla',
            description='Sigla do órgão',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        cargo = Field(**dict(
            name='cargo',
            alias='cargo',
            description='Cargo do gestor',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        telefone = Field(**dict(
            name='telefone',
            alias='telefone',
            description='Telefone do órgão',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        email = Field(**dict(
            name='email',
            alias='email',
            description='E-mail do órgão',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        endereco = Field(**dict(
            name='endereco',
            alias='endereco',
            description='Endereço do orgao',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        coleta = Field(**dict(
            name='coleta',
            alias='coleta',
            description='Intervalo de coleta',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        url = Field(**dict(
            name='url',
            alias='url',
            description='Url da base de dados',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))


        base_metadata = BaseMetadata(
            name='orgaos',
        )

        content_list = Content()
        content_list.append(nome)
        content_list.append(sigla)
        content_list.append(cargo)
        content_list.append(telefone)
        content_list.append(email)
        content_list.append(endereco)
        content_list.append(coleta)
        content_list.append(url)

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

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            response = self.baserest.get(self.lbbase.metadata.name)
            return True
        except:
            return False

orgao_base = OrgaoBase()

class Orgao(orgao_base.metaclass):
    """
    Classe genérica de órgãos
    """
    def __init__(self, **args):
        super(Orgao, self).__init__(**args)
        self.documentrest = orgao_base.documentrest

    def orgao_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(orgao_base.lbbase, self)

    def orgao_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(orgao_base.lbbase, self)

    def create_orgao(self):
        """
        Insert document on base

        :return: Document creation ID
        """

        document = self.orgao_to_json()
        try:
            result = orgao_base.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result

    def search_orgao(self, sigla):
        """
        Busca registro completo do órgao pelo nome
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'sigla' = '"+sigla+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def search_list_orgaos(self):
        """
        Retorna todos os docs da base
        """
        search = Search(
            limit=None
        )
        results = self.documentrest.get_collection(search)

        return results

    def edit_orgao(self, id, doc):
        """
        altera um doc ou path do doc
        """
        results = self.documentrest.update(id, doc)

        return results

    def delete_orgao(self, id):
        """
        Deleta o Órgao apartir do ID
        """
        results = orgao_base.documentrest.delete(id)

        return results
