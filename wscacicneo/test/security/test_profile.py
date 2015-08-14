#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import os
from .. import settings

here = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(here, "../fixtures/")
data_file = os.path.join(data_path, 'users/admin.json')

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from wscacicneo import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.testapp.authorization = ('Basic', ('admin@gov.br', '123'))
        pass


    # def test_check_permission(self):
    #     data = json.loads(open(data_file).read())
    #     has_permission = False
    #     if data["permissao"] == "Administrador":
    #         has_permission = True
    #     self.assertEqual(has_permission, True, msg="Não possui permissão.")

    def test_root(self):
        res = self.testapp.get('/home', status=200)
        self.assertTrue(b'Sistema Super-Gerente' in res.body)

    def test_login_succeeds(self):
        r = self.app.post('/dologin', params={'login': self.user['username'], 'password': self.password})
        resp = self.testapp.post('/orgao/lista')

    def test_good_login(self):
        r = r.follow() # Should only be one redirect to root
        assert 'http://localhost/' == r.request.url
        assert 'Dashboard' in r