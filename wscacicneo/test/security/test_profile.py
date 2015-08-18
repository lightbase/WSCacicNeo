#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import os
from .. import settings
import json

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
data_file = os.path.join(data_path, 'users/admin.json')

class TestProfile(unittest.TestCase):

    def setUp(self):
        from wscacicneo import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_permission_administrator(self):
        data = json.loads(open(data_file).read())
        has_permission = False
        if data["permissao"] == "Administrador":
            has_permission = True
        self.assertEqual(has_permission, True, msg="Não possui permissão.")

    def test_root(self):
        res = self.testapp.get('/home', status=200)
        self.assertTrue(b'Sistema Super-Gerente' in res.body)