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
from wscacicneo.model import base_reports
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()


class ConfReports():

    def __init__(self, nm_base, rest_url=None, response_object=False):
        self.base_nm = nm_base
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.base_reports = base_reports.ReportsBase(nm_base, self.rest_url)
        self.base = self.base_reports.lbbase
        self.documentrest = DocumentREST(self.rest_url, self.base, response_object)


    def get_base(self):
        """
        Retorna todos os documentos da base
        """
        # A resposta nao pode ser object aqui
        self.documentrest.response_object = False
        search = Search(
            limit=None
        )
        get = self.documentrest.get_collection(search_obj=search)

        return get

    def coleta_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(self.base, self)

    def coleta_to_json(self, document):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(document.lbbase, self)

    def create_coleta(self, document):
        """
        Insere dados de coleta
        """
        result = self.documentrest.create(document)

        return result

    def update_coleta(self,id, document):
        """
        Altera dados de coleta
        """
        coleta = self.documentrest.update(id,document)

        return coleta

    def delete_coleta(self,id, document):
        """
        Apaga os dados de coleta
        """
        coleta = self.documentrest.update(id)
        return coleta

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            response = self.baserest.get(self.lbbase.metadata.name)
            return True
        except:
            return False

    def search_orgao(self, sigla):
        """
        Busca registro completo do órgao pelo nome
        :return: obj collection com os dados da base
        """
        data = ['']
        search = Search(
            literal="document->>'sigla' = '"+sigla+"'"
        )
        results = self.documentrest.get_collection(search_obj=search)

        return results

    def get_attribute(self, attr):
        """
        Testa recuperar atributo do Documento
        """
        # A resposta nao pode ser object aqui
        self.documentrest.response_object = False

        search = Search(
            limit=None,
            select=[attr]
        )
        get = self.documentrest.get_collection(search_obj=search)

        return get

    def search_item(self, group ,item, valor):
        """
        Busca registro completo do órgao pelo nome
        :return: obj collection com os dados da base
        """
        search = Search(
            limit= 1,
            literal="document->'"+group+"'->>'"+item+"' = '"+valor+"'"
        )
        print(search._asdict())
        results = self.documentrest.get_collection(search_obj=search)

        return results

