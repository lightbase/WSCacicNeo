#!/usr/env python
# -*- coding: utf-8 -*-asdasd

# # 1. carregar usuário da sessão
# # 2. carregar objeto usuário
# # 3. pegar grupo do usuário

from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils


def groupfinder(userid, request):
    """
    Busca o grupo do usuário de acordo com a sessão

    :param userid:
    :param request:
    :return:
    """
    # Primeiro tenta busca pela chave de API
    userid = request.session.get('userid')
    user_obj = Utils.create_user_obj()
    usuario = user_obj.get_user_by_id(userid)
    permissao = usuario.permissao
    return [permissao]
