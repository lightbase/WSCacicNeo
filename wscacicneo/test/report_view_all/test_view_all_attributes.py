__author__ = 'rodrigo'

import unittest
import json
import os
from .. import settings
import logging

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
log = logging.Logger("TesteVerTodosAtributos")

def dict_depth(d, depth=0):
    if not isinstance(d, dict) or not d:
        return depth
    return max(dict_depth(v, depth+1) for k, v in d.items())

class TestVerTodosAtributos(unittest.TestCase):
    """
    Testa a funcionalidade de agrupamento dos Relatórios
    """
    def setUp(self):
        from wscacicneo import main
        import ast
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.software_list_file= open(data_path + "reports/attribute_list.json")
        # Criando um dicionário com a lista de softwares
        self.software_list = ast.literal_eval(self.software_list_file.read())
        pass

    def test_multiplos_orgaos(self):
        fail=False
        if dict_depth(self.software_list)<2:
            fail=True
        self.assertFalse(fail,"O dicionario deve ter sublistas de software")
    def test_todos_os_orgaos(self):
        fail = False
        if "all" not in self.software_list.keys():
            fail = True
        self.assertFalse(fail,"O dicionario deve possuir o orgao 'all'")
