__author__ = 'rodrigo'

import unittest
import json
import os
from .. import conf

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")

class TestAgrupamentoRelatorio(unittest.TestCase):
    """
    Testa a funcionalidade de agrupamento dos Relatórios
    """
    def setUp(self):
        from webtest import TestApp
        self.testapp = TestApp(conf)
        self.software_list= os.open(data_path + "reports/software_list.txt").read()
        pass

    def test_atributos_versao(self):
        """
        Testa os atributos do nome do programa(suite de escritório)
        """
    def test_atributos_ano(self):
        """
        Testa os atributos do nome do programa(suite de escritório)
        """
    def test_atributos_release(self):
        """
        Testa os atributos do nome do programa(suite de escritório)
        """


