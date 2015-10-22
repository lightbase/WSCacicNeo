#!/usr/env python
# -*- coding: utf-8 -*-

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
from wscacicneo import config

log = logging.getLogger()


class Relacional(object):
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
        conn.close
        return {
            'header': header,
            'rows': rows
        }

    def generate_relacional(self):
        json_relacional = {}
        list_orgaos = ["mpog"]
        headers = {'Content-Type': 'application/json'}
        database_name = "cacic_relacional"
        # Verifica se o Schema já existe
        conn = psycopg2.connect(host="localhost", database="lb_relacional", user="rest", password="rest")
        cur = conn.cursor()
        try:
            cur.execute("DROP SCHEMA "+database_name+" CASCADE;")
            conn.commit()
            conn.close()
            print("dropei")
        except Exception as e:
            print("Drop database error:", e)

        for orgao_name in list_orgaos:
            # Pega  url da base e do orgão
            orgao_base_results = requests.get(config.REST_URL+"/"+orgao_name)
            # Pega e cria json e cria tabela no banco relacional
            orgao_table = json.loads(orgao_base_results.text)
            orgao_table_model = orgao_table["metadata"]["model"]
            orgao_table_model["name_orgao"] = "Text"
            json_data = json.dumps(orgao_table_model)
            relacional_path = "http://127.0.1.1:5000"+"/sqlapi/lightbase/tables/"+database_name
            postRelacional = requests.post(relacional_path, data=json_data, headers=headers)

            # Verifica registro por registro e adiciona o campo name_orgao
            orgao_doc_results = requests.get(config.REST_URL+"/"+orgao_name+"/doc")
            orgao_doc = json.loads(orgao_doc_results.text)
            orgao_doc = orgao_doc["results"]
            for item in orgao_doc:
                item["name_orgao"] = orgao_name
                item.pop("_metadata", None)
                json_data_doc = json.dumps(item)
                relacional_path = "http://127.0.1.1:5000"+"/sqlapi/lightbase/content/"+database_name
                postRelacionalDoc = requests.post(relacional_path, data=json_data_doc, headers=headers)

        return HTTPFound(location=self.request.route_url("conf_csv"))