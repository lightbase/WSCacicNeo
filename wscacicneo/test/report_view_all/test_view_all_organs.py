__author__ = 'rodrigo'

import unittest
import json
import os
from .. import settings
import logging

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
log = logging.Logger("TesteVerTodosOrgaos")
class TestVerTodosOrgaos(unittest.TestCase):
    """
    Testa a funcionalidade de agrupamento dos Relatórios
    """
    def setUp(self):
        from wscacicneo import main
        import ast
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.software_list_file= open(data_path + "reports/software_list.json")
        # Criando um dicionário com a lista de softwares
        self.software_list = ast.literal_eval(self.software_list_file.read())
        pass
    def test_multiplos_orgaos(self):
        fail=False
        if len(self.software_list)>1:
            fail=True
        self.assertFalse(fail,"O dicionario deve possuir o nome do orgao, ou"
                              " 'all' para todos os orgaos")