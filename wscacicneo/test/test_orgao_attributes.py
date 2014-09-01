#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

import unittest
import json
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase

class TestOrgaoBase(unittest.TestCase):
    """
    Testa base do órgão no LB
    """
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.documentrest = OrgaoBase().documentrest

    def test_orgao_attributes(self):
        """
        Insere atributos na base órgãos
        """
        orgao_obj = Orgao(
            nome='Ministério do Planejameiaaaaaaaaanto',
            cargo='cargo',
            coleta='4h',
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117'
        )
        results = orgao_obj.create_orgao()
        var_file = open("results.txt", "w")
        cont = var_file.write(str(results))
        var_file.close()

        self.assertIsInstance(results, int)

    def test_delete_attributes(self):
        """
        Deleta doc apartir do id
        """
        orgao_obj = Orgao(
            nome='Ministério do Planejameiaaaaaaaaanto',
            cargo='cargo',
            coleta='4h',
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117'
        )
        sigla='MPOG'
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        delete = orgao_obj.delete_orgao(id)

        assert(delete == 'DELETED')

    def test_get_attributes(self):
        """
        Retorna todos os doc da base
        """
        search = Orgao.search_list_orgaos

    def test_edit_orgao(self):
        """
        Test Edita Órgão
        """
        orgao_obj = Orgao(
            nome='Ministério do Planejameiaaaaaaaaanto',
            cargo='cargo',
            coleta='1 hora',
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117'
        )
        orgao = dict({
            'nome':'Ministério do Planejameiaaaaaaaaanto',
            'cargo':'cargo',
            'coleta':'4h',
            'sigla':'MPOG',
            'endereco':'Esplanada bloco C',
            'email':'admin@planemaneto.gov.br',
            'telefone':'(61) 2025-4117'
        })
        sigla ='MPOG'
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(orgao)
        edit = orgao_obj.edit_orgao(id, doc)

        assert(edit == 'UPDATED')

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
