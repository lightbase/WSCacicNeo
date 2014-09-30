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
