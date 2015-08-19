#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import os
from .. import settings

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
data_file = os.path.join(data_path, 'users/admin.json')

class TestAttributesBlacklist(unittest.TestCase):

    def setUp(self):
        """
        :return: Inicializa o Servidor de Teste
        """
        from wscacicneo import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_insert_admin_blacklist(self):
        """
        :return: Insere um Item na base Blacklist
        """
        from wscacicneo.model import blacklist
        from wscacicneo.utils.utils import Utils
        from wscacicneo.test.security.test_profile import TestProfile
        ''' Verifica se possui permissão de Admin '''
        TestProfile.test_permission_administrator(self)
        ''' Gera uma string aleatória '''
        random_name = Utils.random_string(8)
        blacklist_obj = blacklist.Blacklist(
            item=random_name
        )
        results = blacklist_obj.create_item()
        total_blackliset = blacklist_obj.search_list_items()
        total_count = total_blackliset.result_count
        self.assertEqual(type(results), int)

    def tearDown(self):
        """
        :return: Apaga dados do Teste
        """
        pass
