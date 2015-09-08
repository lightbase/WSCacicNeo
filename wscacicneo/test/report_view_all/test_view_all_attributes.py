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
    Agrupamento de softwares cadastrados por versão principal
    """
    def setUp(self):
        from wscacicneo import main
        import ast
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.software_list_file= open(data_path + "reports/attribute_list.json")
        # Criando um dicionário com a lista de softwares
        self.organ_list = ast.literal_eval(self.software_list_file.read())
        pass

    def test_list_all(self):
        """
        001 - Testa a existencia de todos os tipos de itens na lista de atributos
        """
        fail = True
        for orgao in self.organ_list.keys():
            if all(item_type in [
                'softwarelist','win32_physicalmemory', 'win32_bios',
                'win32_diskdrive', 'operatingsystem', 'win32_processor'
            ] for item_type in self.organ_list[orgao].keys()):
                fail = False
        self.assertFalse(fail, "Sua lista de atributos deve conter todos os tipos de atributos.")
    def tearDown(self):
        """
        Apaga dados de teste
        """
        pass
