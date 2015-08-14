#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import json
import os
from wscacicneo.model import blacklist
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
data_file = os.path.join(data_path, 'users/admin.json')

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        # from wscacicneo import main
        # app = main({conf})
        from webtest import TestApp
        self.testapp = TestApp(**settings)
        pass
        self.blacklist_base = blacklist.Blacklist()


    def testCheckPermission(self):
        data = json.loads(open(data_file).read())
        has_permission = False
        if data["permissao"] == "Administrador":
            has_permission = True
        self.assertEqual(has_permission, True, msg="Não possui permissão.")

    # def test_root(self):
    #     res = self.testapp.get('/', status=200)
    #     self.assertTrue('Pyramid' in res.body)

    def testCreateBlacklistBase(self):
        """
        Testa criação da base no LB
        """
        result = self.blacklist_base.create_base()
        self.assertEqual(result, 200)

