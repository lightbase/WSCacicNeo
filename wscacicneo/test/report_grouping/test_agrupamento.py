__author__ = 'rodrigo'

import unittest
import json
import os
from .. import settings
import logging

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
log = logging.Logger("TesteAgrupamento")
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
        self.software_list_file= open(data_path + "reports/software_list.json")
        # Criando um dicionário com a lista de softwares
        self.orgao_list = ast.literal_eval(self.software_list_file.read())
        pass

    def test_atributos_versao(self):
        """
        Testa a existência de versão do nome do programa
        """
        fail = False
        for orgao in self.orgao_list.keys():
            if any(s.find('.') >-1 for s in self.orgao_list[orgao].keys()):
                fail = True
        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "O nome de versão não deve possuir ponto.")

    def test_atributos_ano(self):
        """
        Testa a existência de ano de release no nome do programa
        """
        fail = False
        for orgao in self.orgao_list.keys():
            if any(s.find('20') >-1 for s in self.orgao_list[orgao].keys()):
                fail = True
            if any(s.find('19') >-1 for s in self.orgao_list[orgao].keys()):
                fail = True
        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "O ano de release não deve estar presente.")

    def test_atributos_release(self):
        """
        Testa a existência de outras expressões no nome do programa
        """
        release_expressions = [
            "Ultimate",
            "Professional",
            "Standard",
            "Premium",
            "Enterprise",
            "Starter",
            "MUI"
        ]
        fail = False
        # Verifica todas as expressões de release
        for release_expression in release_expressions:
            for orgao in self.orgao_list.keys():
                if any(s.lower().find(release_expression.lower()) >-1 for
                    s in self.orgao_list[orgao].keys()):
                        fail = True

        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "O tipo de release não deve estar presente.")


    def test_atributos_detalhes(self):
        """
        Testa a existência de detalhes entre parênteses
        """
        fail = False
        for orgao in self.orgao_list.keys():
            if any(s.find('(') >-1 for s in self.orgao_list[orgao].keys()):
                fail = True
        self.assertFalse(fail, "Elementos da lista de Software incorretos,\n"
                               "Não devem haver detalhes entre parênteses.")

    def tearDown(self):
        """
        Apaga dados de teste
        """
        pass