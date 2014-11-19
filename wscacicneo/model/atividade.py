#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

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


class AtividadeBase(object):
    """
    Classe para a base de atividades
    """

    def __init__(self, rest_url=None):
        """
        Método construtor da base de atividades
        :param rest_url: URL do Rest
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
        Base no LB
        :return: LB Base object
        """
        tipo = Field(**dict(
            name='tipo',
            description='Tipo de atividade',
            alias='tipo',
            datatype='Text',
            indices=['Textual', 'Ordenado'],
            multivalued=False,
            required=True
        ))

        usuario = Field(**dict(
            name='usuario',
            description='Usuário que realizou a atividade',
            alias='usuario',
            datatype='Text',
            indices=['Textual', 'Ordenado'],
            multivalued=False,
            required=True
        ))

        descricao = Field(**dict(
            name='descricao',
            description='Descrição da atividade',
            alias='descricao',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        data = Field(**dict(
            name='data',
            description='Data de execução da tarefa',
            alias='data',
            datatype='Date',
            indices=['Ordenado'],
            multivalued=False,
            required=True
        ))

        content_list = Content()
        content_list.append(tipo)
        content_list.append(usuario)
        content_list.append(descricao)
        content_list.append(data)

        base_metadata = BaseMetadata(
            name='atividade',
        )

        content_list = Content()
        content_list.append(tipo)

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

atividade_base = AtividadeBase()


class Atividade(atividade_base.metaclass):
    """
    Objeto que contém a ativudade
    """
    def __init__(self, **args):
        super(Atividade, self).__init__(**args)
        self.documentrest = atividade_base.documentrest

    def create_atividade(self):
        """
        Cria entrada no banco para a atividade
        :return: None or insertion result
        """
        document = self.atividade_to_json()
        try:
            result = atividade_base.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result

    def atividade_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(atividade_base.lbbase, self)

    def atividade_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(atividade_base.lbbase, self)