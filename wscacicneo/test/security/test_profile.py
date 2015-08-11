#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import json
import os
from .. import conf

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
data_file = os.path.join(data_path, 'users/admin.json')

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from webtest import TestApp
        self.testapp = TestApp(conf)
        pass

    def testCheckPermission(self):
        data = json.loads(open(data_file).read())
        has_permission = False
        if data["permissao"] == "Administrador":
            has_permission = True
        self.assertEqual(has_permission, True, msg="Não possui permissão.")

    def testAcess(self):
        def test_root(self):
            res = self.app.get('/', status=200)
            self.assertTrue('Pyramid' in res.body)