#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'rodrigo'

import json
import re
import logging
from pyramid.view import view_config
from pyramid.response import Response
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from wscacicneo.model import reports
from wscacicneo.model import all_reports
from wscacicneo.model import descriptions
from wscacicneo.model.reports import Reports
from wscacicneo.search.orgao import SearchOrgao
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import NullDocument
from random import randint
from pyramid.session import check_csrf_token
from pyramid.httpexceptions import HTTPFound
import requests
import psycopg2

log = logging.getLogger()


class RelatorioRelacional(object):
    """
    Métodos básicos do sistema
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    #@view_config(route_name='conf_csv', renderer='../templates/conf_csv.pt')

    def conf_csv(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()

        return {'orgao_doc': result,
                'usuario_autenticado': self.usuario_autenticado
                }

    def lbrelacional_csv(self):
        conn = psycopg2.connect(host="localhost", database="lb_relacional", user="rest", password="rest")
        cur = conn.cursor()
        cur.execute("SELECT * FROM cacic_relacional.cacic_relacional")
        rows = cur.fetchall()
        cur.execute("SELECT * FROM cacic_relacional.cacic_relacional LIMIT 0")
        header = [desc[0] for desc in cur.description]
        filename = 'tabela_relacional' + '.csv'
        self.request.response.content_disposition = 'attachment;filename=' + filename
        return {
            'header': header,
            'rows': rows
        }

