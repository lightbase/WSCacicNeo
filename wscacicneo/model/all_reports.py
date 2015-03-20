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


class AllReports():
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
        COnfiguração da Coleta
        """

        nome_orgao = Field(**dict(
            name='nome_orgao',
            description='Nome do Órgão',
            alias='nome_orgao',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        nome_relatorio = Field(**dict(
            name='nome_relatorio',
            description='Nome do Relatório',
            alias='nome_relatorio',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        data_coleta = Field(**dict(
            name='data_coleta',
            description='Data da Coleta',
            alias='data_coleta',
            datatype='DateTime',
            indices=['Ordenado'],
            multivalued=False,
            required=True
        ))

        total_computadores = Field(**dict(
            name='total_computadores',
            description='Total de Computadores',
            alias='total_computadores',
            datatype='Integer',
            indices=['Ordenado'],
            multivalued=False,
            required=True
        ))

        nome_item = Field(**dict(
            name='nome_item',
            description='Nome do Item',
            alias='nome_item',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        quantidade_item = Field(**dict(
            name='quantidade_item',
            description='Quantidades total do item',
            alias='quantidade_item',
            datatype='Integer',
            indices=['Ordenado'],
            multivalued=False,
            required=True
        ))

        descricao_item = Field(**dict(
            name='descricao_item',
            description='Descrição',
            alias='descricao_item',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))


        """
        GROUP Sistema Operacional
        """
        ItensGroup_content = Content()
        ItensGroup_content.append(nome_item)
        ItensGroup_content.append(quantidade_item)
        ItensGroup_content.append(descricao_item)

        ItensGroup_metadata = GroupMetadata(
            name='ItensGroup',
            alias='ItensGroup',
            description='Grupo de Itens',
            multivalued=True
        )

        ItensGroup = Group(
            metadata=ItensGroup_metadata,
            content=ItensGroup_content
        )

        base_metadata = BaseMetadata(
            name='all_reports'
        )

        content_list = Content()
        content_list.append(nome_orgao)
        content_list.append(nome_relatorio)
        content_list.append(data_coleta)
        content_list.append(total_computadores)
        content_list.append(ItensGroup)

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
        self.baserest.response_object = True
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


allreports = AllReports()


class ReportsAll(allreports.metaclass):
    """
    Classe genérica de Reports
    """
    def __init__(self, **args):
        super(ReportsAll, self).__init__(**args)
        self.documentrest = allreports.documentrest

    @property
    def coleta(self):
        """
        Tempo de coleta
        :return: Retorna o valor gravado ou o mínimo de 3 horas
        """
        col = allreports.metaclass.coleta.__get__(self)
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
        allreports.metaclass.coleta.__set__(self, value)

    def allreports_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(allreports.lbbase, self)

    def allreports_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(allreports.lbbase, self)

    def create_doc_allreports(self):
        """
        Insert document on base

        :return: Document creation ID
        """

        document = self.allreports_to_json()
        try:
            result = allreports.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None

        return result

    def search_doc_allreports(self, sigla):
        """
        Busca registro completo do órgao pelo nome
        :return: obj collection com os dados da base
        """
        search = Search(
            literal="document->>'sigla' = '"+sigla+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def search_list_allreports(self):
        """
        Retorna todos os docs da base
        """
        search = Search(
            limit=None
        )
        results = self.documentrest.get_collection(search)

        return results

    def edit_allreports(self, id, doc):
        """
        altera um doc ou path do doc
        """
        results = self.documentrest.update(id, doc)

        return results

    def delete_allreports(self, id):
        """
        Deleta o allreports apartir do ID
        """
        results = allreports.documentrest.delete(id)

        return results
