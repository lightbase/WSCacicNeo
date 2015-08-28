#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

import datetime
import logging
from datetime import date
from requests.exceptions import HTTPError
from wscacicneo import config
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from wscacicneo.model import coleta_manual
from wscacicneo.model import reports
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy
from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc
from wscacicneo.lib import convert


log = logging.getLogger()


class CreateReports():


    def __init__(self, m_base):
        self.report = reports.Reports(nm_base)


    def total_computers(self):
        """
        Retorna a quantidade total de computadores do órgão específico 
        """
        total = self.report.get_base_orgao()

        return total.result_count


    def datetime(self):
        """
        Retorna data e hora do relatorio 
        """
        date = datetime.datetime.now()
        date_report = {
            "day"    : date.day,
            "month"  : date.month,
            "year"   : date.year,
            "hour"   : date.hour,
            "minute" : date.minute,
            "second" : date.second
        }
        return date_report
