#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

import unittest
import json
import configparser
import os
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from pyramid import testing

class TestReportsBase(unittest.TestCase):


    def setUp(self):
        self.rest_url = 'http://api.brlight.net/api'
        self.nm_base = 'test_base_reports'

    def test_create_base(self):
        """
        Testa criação da base no LB
        """
        reports = base_reports.ReportsBase(self.nm_base, self.rest_url)
        lbbase = reports.lbbase
        self.assertIsInstance(lbbase, Base)

        retorno = reports.create_base()
        self.assertIsInstance(retorno, Base)

    def test_insert_doc(self):
        """
        Insere registros na base
        """
        document = dict({"item":"processador", "amount": "50"})
        document_format = json.dumps(document)
        results = config_reports.ConfReports(self.nm_base, self.rest_url, response_object=False).create_coleta(document_format)

        self.assertIsInstance(results, int)

    def tearDown(self):
        pass
