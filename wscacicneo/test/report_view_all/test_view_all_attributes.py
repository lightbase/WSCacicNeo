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
        self.software_list = ast.literal_eval(self.software_list_file.read())
        pass

    def test_agrupamento(self):
        """
        DADO QUE: Sou usuário do sistema;
        QUERO: Agrupar os softwares coletados;
        PELOS SEGUINTES ATRIBUTOS: Nome do software.
        """
        assert False

    def test_agrupamento_versao(self):
        """
        Dado que: O sistema tenha recebido dados dos agentes de coleta;
        Quando: Os softwares presentes em meu sistema possuam vários componentes que o definam, como “releases” e subversões;
        Então: O sistema deverá apresentar um relatório com os softwares agrupados somente pelo indicador de sua versão principal.
        """
        assert False

    def tearDown(self):
        """
        Apaga dados de teste
        """
        pass
