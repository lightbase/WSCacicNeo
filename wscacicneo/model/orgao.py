#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from requests.exceptions import HTTPError
from wscacicneo import WSCacicNeo
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv

class OrgaoBase(WSCacicNeo):
    """
    Classe para a base de órgãos
    """
    def __init__(self):
        """
        Método construtor
        """
        WSCacicNeo.__init__(self)
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=True)

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
        #print(response.status_code)
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

orgao_base = OrgaoBase()

class Orgao(orgao_base.metaclass):
    """
    Classe genérica de órgãos
    """
    def __init__(self, **args):
        super(Orgao, self).__init__(**args)

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
        except HTTPError, err:
            log.error(err.strerror)
            return None

        return result
