__author__ = 'rodrigo'

import unittest
import json
import os
from .. import settings

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")

class TestAgrupamentoRelatorio(unittest.TestCase):
    """
    Testa a funcionalidade de agrupamento dos Relatórios
    """
    def setUp(self):
        from wscacicneo import main
        import ast
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.software_list_file= open(data_path + "reports/software_list.txt")
        # Criando um dicionário com a lista de softwares
        self.software_list = ast.literal_eval(self.software_list_file.read())
        pass

    def test_atributos_versao(self):
        """
        Testa a existência de versão do nome do programa
        """
        fail = False
        if any(s.find('.') >-1 for s in self.software_list.keys().__str__()):
            fail = True
        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "O nome de versão não deve possuir ponto.")

    def test_atributos_ano(self):
        """
        Testa a existência de ano de release no nome do programa
        """
        fail = False
        if any(s.find('20') >-1 for s in self.software_list.keys().__str__()):
            fail = True
        if any(s.find('19') >-1 for s in self.software_list.keys().__str__()):
            fail = True
        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "O ano de release não deve estar presente.")

    def test_atributos_release(self):
        """
        Testa oa existência de outras expressões no nome do programa
        """
        fail = False
        if any(s.find('Ultimate') >-1 for
               s in self.software_list.keys().__str__()):
            fail = True
        if any(s.find('Professional') >-1 for
               s in self.software_list.keys().__str__()):
            fail = True
        if any(s.find('Standard') >-1 for
               s in self.software_list.keys().__str__()):
            fail = True
        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "O tipo de release não deve estar presente.")


