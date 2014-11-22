#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import logging
import datetime
from requests.exceptions import HTTPError
from wscacicneo import config
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()


class NotifyBase():
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
        LB Base de Notify
        """
        orgao = Field(**dict(
            name='orgao',
            description='Órgão referente a notrificção',
            alias='orgao',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        data_coleta = Field(**dict(
            name='data_coleta',
            alias='data_coleta',
            description='data da coleta notificada',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        notify = Field(**dict(
            name='notify',
            alias='notify',
            description='tipo de notificação',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        coment = Field(**dict(
            name='coment',
            alias='coment',
            description='comentario',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        status = Field(**dict(
            name='status',
            alias='status',
            description='status da notificação',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        base_metadata = BaseMetadata(
            name='notify',
        )
        content_list = Content()
        content_list.append(orgao)
        content_list.append(data_coleta)
        content_list.append(notify)
        content_list.append(coment)
        content_list.append(status)

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

notify_base = NotifyBase()


class Notify(notify_base.metaclass):
    """
    Classe genérica de órgãos
    """
    def __init__(self, **args):
        super(Notify, self).__init__(**args)
        self.documentrest = notify_base.documentrest

    @property
    def data_coleta(self):
        """
        Getter da data
        """
        return notify_base.metaclass.data_coleta.__get__(self)

    @data_coleta.setter
    def data_coleta(self, value):
        """
        Ajusta o valor da data se for nulo
        :param value:
        """
        if value is None:
            value = datetime.datetime.now().strftime("%d/%m/%Y")
        else:
            value = value.strftime("%d/%m/%Y")

        notify_base.metaclass.data_coleta.__set__(self, value)

    def notify_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(notify_base.lbbase, self)

    def notify_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(notify_base.lbbase, self)

    def create_notify(self):
        """
        Insert document on base

        :return: Document creation ID
        """

        document = self.notify_to_json()
        try:
            result = notify_base.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result

    def search_notify(self, orgao):
        """
        Busca registro completo do notify pelo id
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'orgao' = '"+orgao+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def search_list_notify(self):
        """
        Retorna todos os docs da base
        """
        search = Search(
            limit=None
        )
        results = self.documentrest.get_collection(search)

        return results

    def edit_notify(self, id, doc):
        """
        altera um doc ou path do doc
        """
        results = self.documentrest.update(id, doc)

        return results

    def delete_notify(self, id):
        """
        Deleta o Órgao apartir do ID
        """
        results = self.documentrest.delete(id)

        return results
