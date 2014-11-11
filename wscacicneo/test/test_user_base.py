#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
from wscacicneo.model import user
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv

class TestUserBase(unittest.TestCase):
    """
    Testa base do órgão no LB
    """
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.rest_url = 'http://api.brlight.net/api'

    def test_create_base(self):
        """
        Testa criação da base no LB
        """
        user_base = user.UserBase(rest_url=self.rest_url)
        lbbase = user_base.lbbase
        self.assertIsInstance(lbbase, Base)

        retorno = user_base.create_base()
        self.assertIsInstance(retorno, Base)

        #retorno = user_base.remove_base()
        #self.assertTrue(retorno)

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
