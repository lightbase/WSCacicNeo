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

    def __init__(self, nm_base, rest_url=None):
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.base = coleta_manual.ColetaManualBase(nm_base, self.rest_url).lbbase
        print(type(self.base))
        self.documentrest = DocumentREST(self.rest_url, self.base, response_object=True)


    def get_base_orgao(self):
        """
        retorna todos os documentos da base
        """
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

    def coleta_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(nm_base.lbbase, self)

    def create_coleta(self, document):
        """
        Insere dados de coleta
        """
        document = self.coleta_to_json()
        try:
            coleta = self.documentrest.create(document)
        except HTTPError as err:
            log.error(err.strerror)
            return None
        
        return coleta

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