#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

from requests.exceptions import HTTPError
from wscacicneo import config
import logging
import requests
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()


class BlacklistBase(object):
    """
    Classe para a base de órgãos
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
        LB Base do órgão
        """
        item = Field(**dict(
            name='item',
            description='Nome do item que será adicionado a lista.',
            alias='nome',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=True
        ))

        base_metadata = BaseMetadata(
            name='blacklist',
        )

        content_list = Content()
        content_list.append(item)

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


blacklist_base = BlacklistBase()


class Blacklist(blacklist_base.metaclass):
    """
    Classe genérica da blacklist
    """
    def __init__(self, **args):
        super(Blacklist, self).__init__(**args)
        self.documentrest = blacklist_base.documentrest

    def blacklist_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """
        return conv.document2dict(blacklist_base.lbbase, self)

    def blacklist_to_json(self):
        """
        Convert object to json
        :return:
        """
        return conv.document2json(blacklist_base.lbbase, self)

    def create_item(self):
        """
        Insert document on base

        :return: Document creation ID
        """

        document = self.blacklist_to_json()
        try:
            result = blacklist_base.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result

    def search_item(self, item):
        """
        Busca registro completo do usuário pela matricula
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'item' = '"+item+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def search_list_items(self):
        """
        Retorna todos os docs da base
        """
        search = Search(
            limit=None
        )
        results = self.documentrest.get_collection(search)

        return results

    def edit_item(self, id, doc):
        """
        altera um doc ou path do doc
        """
        results = self.documentrest.update(id, doc)

        return results

    def get_item_by_id(self, id_item):
        """
        Retorna um documento a partir do id
        """

        results = self.documentrest.get(id_item)

        return results

    def delete_item(self, id):
        """
        Deleta o Órgao apartir do ID
        """
        results = blacklist_base.documentrest.delete(id)

        return results