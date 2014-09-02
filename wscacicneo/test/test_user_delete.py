   #!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import json
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase

class TestUserDelete(unittest.TestCase):
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.documentrest = UserBase().documentrest

    
    def test_delete_attributes(self):
        """
        Deleta doc apartir do id
        """
        user_obj = User(
            nome='test1',
            matricula='test1',
            email='test1@gov.br',
            telefone='test1',
            orgao='test1',
            cargo='test1',
            setor='test1',
            permissao='Administrador',
            senha='123'
        )
        matricula_user='test1'
        search = user_obj.search_user(matricula_user)
        id = search.results[0]._metadata.id_doc
        delete = user_obj.delete_user(id)

        assert(delete == 'DELETED')
        
    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
