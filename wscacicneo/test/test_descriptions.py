#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
from ..model import descriptions


class TestDescriptions(unittest.TestCase):
    """
    Testa base de descrições de campos
    """

    def setUp(self):
        self.desc_base = descriptions.DescriptionsBase()

    def test_create_base(self):
        """
        Testa criação da base de descrições
        """
        self.desc_base.create_base()
        self.desc_base.remove_base()

    def test_load_file(self):
        """
        Testa carga de arquivos
        """
        self.desc_base.create_base()
        self.desc_base.load_static()
        self.desc_base.remove_base()

    def tearDown(self):
        pass