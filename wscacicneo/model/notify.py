#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import logging
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
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
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

        id_coleta = Field(**dict(
            name='id_coleta',
            alias='id_coleta',
            description='id da coleta notificada',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        notify = Field(**dict(
            name='notify',
            alias='notify',
            description='campo de notificações',
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
        content_list.append(id_coleta)
        content_list.append(notify)
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
            self.baserest.response_object = False
            response = self.baserest.get(self.lbbase.metadata.name)
            self.baserest.response_object = True
            return True
        except:
            return False

notify_base = NotifyBase()


class Notify(notify_base.metaclass):
    """
    Classe genérica de órgãos
    """
    def __init__(self, **args):
        super(Notify, self).__init__(**args)
        self.documentrest = notify_base.documentrest

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

    def search_notify(self, sigla):
        """
        Busca registro completo do notify pelo id
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'sigla' = '"+orgao+"'"
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
        results = orgao_base.documentrest.delete(id)

        return results
