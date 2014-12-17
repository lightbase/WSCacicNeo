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


class EmailBase(object):
    """
    Classe para a base de email
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
        LB Base de email
        """
        usuario = Field(**dict(
            name='usuario',
            description='Usuario',
            alias='Usuario',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        to = Field(**dict(
            name='to',
            description='Destino do email',
            alias='to',
            datatype='Text',
            indices=['Textual'],
            multivalued=True,
            required=True
        ))

        reply_to = Field(**dict(
            name='reply_to',
            alias='reply_to',
            description='reply_to',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        subject = Field(**dict(
            name='subject',
            alias='Assunto',
            description='Assunto do e-mail',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        body = Field(**dict(
            name='body',
            alias='body',
            description='Corpo do e-mail',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        headers = Field(**dict(
            name='headers',
            alias='headers',
            description='headers',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        data_send = Field(**dict(
            name='data_send',
            alias='data_send',
            description='Data de envio',
            datatype='datetime',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        status = Field(**dict(
            name='status',
            alias='status',
            description='status',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        hidden_destination = Field(**dict(
            name='hidden_destination',
            alias='hd',
            description='hd',
            datatype='text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        base_metadata = BaseMetadata(
            name='email',
        )

        content_list = Content()
        content_list.append(usuario)
        content_list.append(to)
        content_list.append(reply_to)
        content_list.append(subject)
        content_list.append(body)
        content_list.append(headers)
        content_list.append(data_send)
        content_list.append(status)
        content_list.append(hidden_destination)

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

email_base = EmailBase()


class Email(email_base.metaclass):
    """
    Classe genérica de órgãos
    """
    def __init__(self, **args):
        super(Email, self).__init__(**args)
        self.documentrest = email_base.documentrest

    @property
    def coleta(self):
        """
        Tempo de coleta
        :return: Retorna o valor gravado ou o mínimo de 3 horas
        """
        col = email_base.metaclass.coleta.__get__(self)
        if col is None:
            return 3
        else:
            return col

    @coleta.setter
    def coleta(self, value):
        """
        Setter
        """
        value = int(value)
        email_base.metaclass.coleta.__set__(self, value)

    def email_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(email_base.lbbase, self)

    def email_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(email_base.lbbase, self)

    def email_post(self):
        """
        Insert document on base

        :return: Document creation ID
        """

        document = self.email_to_json()
        try:
            result = email_base.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result


