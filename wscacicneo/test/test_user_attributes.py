#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

import unittest
import json
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase

class TestUserBase(unittest.TestCase):
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
            nome='Fernando Goku',
            matricula='12311231',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117',
            orgao='Ministério do Pppp',
            cargo='Gestor de TI',
            setor='Setor de TI',
            permissao='administrador'
        )
        results = user_obj.create_user()
        var_file = open("results.txt", "w")
        cont = var_file.write(str(results))
        var_file.close()

        self.assertIsInstance(results, int)

    def test_delete_attributes(self):
        """
        Deleta doc apartir do id
        """
        user_obj = User(
            nome='Fernando Goku',
            matricula='12311231',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117',
            orgao='Ministério do Pppp',
            cargo='Gestor de TI',
            setor='Setor de TI',
            permissao='administrador'
        )
        matricula_user='12311231'
        search = user_obj.search_user(matricula_user)
        id = search.results[0]._metadata.id_doc
        delete = user_obj.delete_user(id)

        assert(delete == 'DELETED')

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
            nome='Fernando Goku',
            matricula='12311231',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117',
            orgao='Ministério do Pppp',
            cargo='Gestor de TI',
            setor='Setor de TI',
            permissao='administrador'
        )
        user = {
            'nome' :'Goku',
            'matricula':'12311231',
            'email':'admin@planemaneto.gov.br',
            'telefone':'(61) 2025-4117',
            'orgao':'Ministério do Pppp',
            'cargo':'Gestor de TI',
            'setor':'Setor de TI',
            'permissao':'administrador'
        }
        matricula_user='12311231'
        search = user_obj.search_user(matricula_user)
        id = search.results[0]._metadata.id_doc
        print("KKKKKKKKKKKKKKKKKKKKK",id)
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)

        assert(edit == 'UPDATED')

    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
