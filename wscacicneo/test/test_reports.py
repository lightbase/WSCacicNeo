#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
import json
from wscacicneo.model import reports
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv

class TestRelatorio(unittest.TestCase):
    """
    Testa base do órgão no LB
    """
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.rest_url = 'http://api.brlight.net/api'
        self.nm_base = 'ministerioaaaa'

    def test_get_doc_base(self):
        """
        Testa busca o documento completo da base
        """
        get_doc = reports.Reports(self.nm_base, self.rest_url)
        lbbase = get_doc.get_base_orgao()
        self.assertGreater(len(lbbase.results), 0)

    def test_get_attribute(self):
        """
        Teste recuperar um atributo específico da base
        """
        get_doc = reports.Reports(self.nm_base, self.rest_url)
        coleta = get_doc.get_base_orgao()
        hd = get_doc.get_attribute('operatingsystem')
        self.assertGreater(len(hd.results), 0)

    def test_count_attribute(self):
        """
        Método que retora um dicionário de atributos agrupados com o valor
        de ocorrência de cada um deles
        """
        get_doc = reports.Reports(self.nm_base, self.rest_url)
        coleta = get_doc.get_base_orgao()
        hd = get_doc.get_attribute('win32_processor')
        self.assertGreater(len(hd.results), 0)

        hd_count = get_doc.count_attribute('win32_processor', 'win32_processor_manufacturer')
        fd = open('/tmp/teste.json', 'w+')
        fd.write(json.dumps(hd_count))
        fd.close()
        self.assertGreater(len(hd_count.keys()), 0)

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
