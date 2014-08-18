#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
from wscacicneo.model import orgao
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
        pass

    def test_base(self):
        """
        Testa criação do objeto base no LB
        """
        orgao_base = orgao.OrgaoBase()
        lbbase = orgao_base.lbbase
        self.assertIsInstance(lbbase, Base)

        fd = open('/tmp/orgao_base.json', 'w+')
        fd.write(lbbase.json)
        fd.close()
        self.assertIsInstance(lbbase, Base)
        j = lbbase.json
        b = conv.json2base(j)
        self.assertIsInstance(b, Base)

    def test_create_base(self):
        """
        Testa criação da base no LB
        """
        orgao_base = orgao.OrgaoBase()
        lbbase = orgao_base.lbbase
        self.assertIsInstance(lbbase, Base)

        retorno = orgao_base.create_base()
        self.assertIsInstance(retorno, Base)

        retorno = orgao_base.remove_base()
        self.assertTrue(retorno)

    def test_orgao_metaclass(self):
        """
        testa atribuição de metaclass
        """
        orgao_base = orgao.OrgaoBase()
        lbbase = orgao_base.lbbase
        self.assertIsInstance(lbbase, Base)

        self.assertIsNotNone(orgao_base.metaclass)

    def test_orgao_attributes(self):
        """
        Testa verificação de atributos
        """
        orgao_obj = orgao.Orgao(
            nome='Ministério do Planejamento',
            cargo='cargo',
            coleta='4h',
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117'
        )
        self.assertIsInstance(orgao_obj, orgao.Orgao)
        self.assertEqual(orgao_obj.nome, 'Ministério do Planejamento')
        self.assertEqual(orgao_obj.cargo, 'Gestor')

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
