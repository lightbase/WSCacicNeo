#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
from wscacicneo.model import reports
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv

class TestOrgaoBase(unittest.TestCase):
    """
    Testa base do órgão no LB
    """
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.rest_url = 'http://api.brlight.net/api'
        self.nm_base = 'coleta_manual'

    def test_get_doc_base(self):
        """
        Testa busca o documento completo da base
        """
        get_doc = reports.Reports(self.rest_url, self.nm_base)
        lbbase = get_doc.get_base_orgao

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
