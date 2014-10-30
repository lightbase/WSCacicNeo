#!/usr/env python
# -*- coding: utf-8 -*-asdasd

# # 1. carregar usuário da sessão
# # 2. carregar objeto usuário
# # 3. pegar grupo do usuário

from wscacicneo.model.user import User


def groupfinder(userid, request):
    user_obj = User(
        nome = 'usuario',
        matricula = '000000',
        email = 'usuario@gov.br',
        orgao = 'mpog',
        telefone = '(11)1111-1111',
        cargo = 'adm',
        setor = 'ti',
        permissao = 'Administrador',
        senha = '123',
        favoritos = ['favoritos']
    )
    usuario = user_obj.search_user_by_email(userid)
    permissao = usuario.results[0].permissao
    return [permissao]
