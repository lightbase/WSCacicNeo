#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import json
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase

class TestUserAttributes(unittest.TestCase):
    """
    Testa base do órgão no LB
    """
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.documentrest = UserBase().documentrest

    def test_user_attributes(self):
        """
        Insere atributos na base users
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
        results = user_obj.create_user()
        var_file = open("results.txt", "w")
        cont = var_file.write(str(results))
        var_file.close()

        self.assertIsInstance(results, int)


    def test_get_attributes(self):
        """
        Retorna todos os doc da base
        """
        search = User.search_list_users

    def test_edit_user(self):
        """
        Test Edita Usuário
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
        user = {
            'nome' :'test1',
            'matricula':'test1',
            'email':'test1@gov.br',
            'telefone':'test1',
            'orgao':'test1',
            'cargo':'test1',
            'setor':'test1',
            'permissao':'Administrador',
            'senha':'123'
        }
        matricula_user='test1'
        search = user_obj.search_user(matricula_user)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)

        assert(edit == 'UPDATED')

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
