#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import configparser
import os
from wscacicneo.model import base_bk
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from pyramid import testing

class TestBKBase(unittest.TestCase):


    def setUp(self):
        self.rest_url = 'http://api.brlight.net/api'

    def test_create_base(self):
        """
        Testa criação da base no LB
        """
        bk= base_bk.BaseBackup(self.rest_url)
        lbbase = bk.lbbase
        self.assertIsInstance(lbbase, Base)

        retorno = bk.create_base()
        self.assertIsInstance(retorno, Base)

    def tearDown(self):
        pass
