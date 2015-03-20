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
from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc
from wscacicneo.lib import convert


log = logging.getLogger()


class CreateReports():


    def __init__(self):
        pass



    def report_attributes(self, attr):
        """
        Cria lista de atributos para o relatorio  
        Note : attr deve ser uma lista
        """
        if type(attr) is list:
            pass
        else:
            return str('vai da pau')
