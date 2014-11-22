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
from wscacicneo.model import coleta_manual
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()


class Reports():

    def __init__(self, nm_base, rest_url=None, response_object=True):
        self.base_nm = nm_base
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.coleta_manual_base = coleta_manual.ColetaManualBase(nm_base, self.rest_url)
        self.base = self.coleta_manual_base.lbbase
        self.documentrest = DocumentREST(self.rest_url, self.base, response_object)


    def get_base_orgao(self):
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

        return conv.document2dict(coleta_base.lbbase, self)

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

    def get_attribute(self, attr):
        """
        Testa recuperar atributo do Documento
        """
        # A resposta nao pode ser object aqui
        self.documentrest.response_object = False

        # FIXME: Adicionar lista de atributos obrigatórios nos campos que vao retornar na busca
        # Referência: http://dev.lightbase.cc/projects/liblightbase/repository/revisions/master/entry/liblightbase/lbbase/content.py#L34

        # A busca deve obrigatoriamente retornar todos os atributos obrigatórios
        search = Search(
            limit=None,
            select=[attr, "data_coleta"]
        )
        get = self.documentrest.get_collection(search_obj=search)

        return get

    def count_attribute(self, attr, child=None):
        """
        retorna dicionário de atributos agrupados por contador
        """
        attr_dict = self.get_attribute(attr)
        results = attr_dict.results

        saida = dict()
        for elm in results:
            if child:
                parent = getattr(elm, attr)
                attribute = getattr(parent, child)
            else:
                attribute = getattr(elm, attr)

            if saida.get(attribute):
                saida[attribute] = saida.get(attribute) + 1
            else:
                saida[attribute] = 1

        return saida
