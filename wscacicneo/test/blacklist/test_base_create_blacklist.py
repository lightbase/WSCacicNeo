#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import os
from .. import settings

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
data_file = os.path.join(data_path, 'users/admin.json')

class TestBaseBlacklist(unittest.TestCase):

    def setUp(self):
        """
        :return: Inicializa o Servidor de Teste
        """
        from wscacicneo import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_create_base(self):
        """
        :return: Cria a base no LB
        """
        from wscacicneo.model import blacklist
        from liblightbase.lbbase.struct import Base

        blacklist_base = blacklist.BlacklistBase()
        result = blacklist_base.create_base()
        self.assertEqual(result, True)

    def tearDown(self):
        """
        :return: Apaga dados do Teste
        """
        pass

