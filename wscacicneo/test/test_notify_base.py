#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

import unittest
import configparser
import os
from wscacicneo.model import notify
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from pyramid import testing

class NotifyBase(unittest.TestCase):


    def setUp(self):
        self.rest_url = 'http://api.brlight.net/api'

    def test_create_base(self):
        """
        Testa criação da base no LB
        """
        notify_base = notify.NotifyBase(self.rest_url)
        lbbase = notify_base.lbbase
        self.assertIsInstance(lbbase, Base)

        retorno = notify_base.create_base()
        self.assertIsInstance(retorno, Base)

    def tearDown(self):
        pass
