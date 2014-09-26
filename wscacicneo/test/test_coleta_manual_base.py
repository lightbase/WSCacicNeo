#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import configparser
import os
from wscacicneo.model import coleta_manual
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from pyramid import testing

class TestColetaManualBase(unittest.TestCase):


    def setUp(self):
        self.rest_url = 'http://api.brlight.net/api'

    def test_create_base(self):
        """
        Testa criação da base no LB
        """
        coletaManualBase = coleta_manual.ColetaManualBase(self.rest_url)
        lbbase = coletaManualBase.lbbase
        self.assertIsInstance(lbbase, Base)

        retorno = coletaManualBase.create_base()
        self.assertIsInstance(retorno, Base)

    def tearDown(self):
        pass