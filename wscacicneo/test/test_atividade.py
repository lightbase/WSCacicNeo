#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
import datetime
from pyramid import testing
from . import settings
from ..model import atividade


class TestAtividade(unittest.TestCase):
    """
    Testa base de atividades
    """

    def setUp(self):
        """
        Carrega atributos
        """
        self.config = testing.setUp(settings=settings)
        self.atividade_base = atividade.AtividadeBase()

    def test_create_base(self):
        """
        Testa criação da Base de atividades
        """
        result = self.atividade_base.create_base()
        self.assertIsNotNone(result)

        result = self.atividade_base.remove_base()
        self.assertTrue(result)

    def test_create_atividade(self):
        """
        Testa criação de atividade
        """
        result = self.atividade_base.create_base()
        self.assertIsNotNone(result)

        # Testa criação da atividade
        ativ = atividade.Atividade(
            tipo='coleta',
            usuario='WSCBot',
            descricao='Inserção de coleta',
            data=datetime.datetime.now()
        )

        ativ_dict = ativ.atividade_to_dict()
        self.assertEqual(ativ.tipo, ativ_dict['tipo'])

        doc = ativ.create_atividade()
        self.assertIsNotNone(doc)

        result = self.atividade_base.remove_base()
        self.assertTrue(result)

    def tearDown(self):
        """
        Apaga atributos
        """
        pass