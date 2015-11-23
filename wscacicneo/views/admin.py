#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
from ..utils.utils import Utils
from ..model import orgao
from pyramid.exceptions import HTTPNotFound, HTTPBadRequest


class AdminView(object):
    """
    Tarefas administrativas
    """
    def __init__(self, request):
        """
        Método construtor

        :param request: Objeto da requisição
        :return:
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid')
        )

    def admin_index(self):
        """
        Página de administração
        """
        return {
            'usuario_autenticado': self.usuario_autenticado,
            'orgao_base': orgao.orgao_base.lbbase.metadata.name
        }

    def admin_bases_update(self):
        """
        Atualiza base com o nome fornecido
        """
        nm_base = self.request.matchdict.get('nm_base')

        if nm_base == orgao.orgao_base.lbbase.metadata.name:
            # Atualiza a base do órgão
            try:
                orgao.orgao_base.update_base()
            except IOError as e:
                raise HTTPBadRequest(e.message)
        else:
            return HTTPNotFound

        return {}
