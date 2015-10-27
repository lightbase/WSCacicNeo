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
        self.host = config.DB_HOST
        self.database = config.DB_NAME
        self.user_db = config.DB_USER
        self.password_db = config.DB_PASS
        self.lbrelacional_url = config.LBRELACIONAL_URL
        self.schema_name = 'cacic_relacional'

    #@view_config(route_name='conf_csv', renderer='../templates/conf_csv.pt')

    def conf_csv(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()

        # Verifica se o Schema já existe
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
        cur = conn.cursor()
        # Verifica se a base já foi criada
        cur.execute("SELECT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'cacic_relacional');")
        for item in cur:
            check_exists = item
        check_exists = check_exists[0]

        return {'orgao_doc': result,
                'usuario_autenticado': self.usuario_autenticado,
                'table_exists': check_exists
                }

    def lbrelacional_csv(self):
        try:
            listaorgaos = self.request.params.getall('orgao')
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
            cur = conn.cursor()
            if len(listaorgaos) == 1:
                cur.execute("SELECT * FROM "+self.schema_name+"."+self.schema_name+" WHERE name_orgao = '{0}'".format(listaorgaos[0]))
            else:
                cur.execute("SELECT * FROM "+self.schema_name+"."+self.schema_name+" WHERE name_orgao in {0}".format(tuple(listaorgaos)))
            rows = cur.fetchall()
            cur.execute("SELECT * FROM "+self.schema_name+"."+self.schema_name+" LIMIT 0")
            header = [desc[0] for desc in cur.description]
            filename = 'tabela_relacional' + '.csv'
            self.request.response.content_disposition = 'attachment;filename=' + filename
            conn.close()
            return {
                'header': header,
                'rows': rows
            }
        except Exception as error:
            session = self.request.session
            session.flash('É necessário gerar o banco de dados relacional antes de exportá-lo!', queue="error")
            return HTTPFound(location=self.request.route_url("conf_csv"))

    def generate_relacional(self):
        # Verifica se o Schema já existe
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
        cur = conn.cursor()
        # Verifica se a base já foi criada
        cur.execute("SELECT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'cacic_relacional');")
        for item in cur:
            check_exists = item
        check_exists = check_exists[0]
        if check_exists:
            cur.execute("DELETE FROM cacic_relacional.cacic_relacional_softwarelist; ")
            cur.execute("DELETE FROM cacic_relacional.cacic_relacional; ")
            conn.commit()

        list_orgaos = []
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()
        for item in result:
            list_orgaos.append(item.nome)
        headers = {'Content-Type': 'application/json'}

        for orgao_name in list_orgaos:
            # Pega  url da base e do orgão
            orgao_base_results = requests.get(config.REST_URL+"/"+orgao_name)
            # Pega e cria json e cria tabela no banco relacional
            orgao_table = json.loads(orgao_base_results.text)
            orgao_table_model = orgao_table["metadata"]["model"]
            orgao_table_model["name_orgao"] = "Text"
            try:
                verify_hash = orgao_table["metadata"]["model"]["hash_machine"]
            except:
                orgao_table_model["hash_machine"] = "Text"

            json_data = json.dumps(orgao_table_model)
            if not check_exists:
                session = self.request.session
                session.flash('A tabela foi gerada com sucesso.', queue="success")
                session.flash('Clique em gerar para gerar o conteúdo.', queue="warning")
                relacional_path = self.lbrelacional_url+"/sqlapi/lightbase/tables/"+self.schema_name
                requests.post(relacional_path, data=json_data, headers=headers)
                select = self.try_select()
                while not select:
                    select = self.try_select()
                    if select:
                        cur.execute("DELETE FROM cacic_relacional.cacic_relacional_softwarelist; ")
                        cur.execute("DELETE FROM cacic_relacional.cacic_relacional; ")
                        conn.commit()
                        conn.close()
                return HTTPFound(location=self.request.route_url("conf_csv"))
            else:
                conn.close()
                try:
                    self.post_content_relacional(orgao_name, headers)
                    session = self.request.session
                    session.flash('O banco de dados relacional foi gerado com sucesso', queue="success")
                    return HTTPFound(location=self.request.route_url("conf_csv"))
                except Exception as e:
                    logging.error("Erro ao criar conteúdo: ", e)
                    session = self.request.session
                    session.flash('O banco de dados relacional foi gerado com sucesso', queue="success")
                    return HTTPFound(location=self.request.route_url("conf_csv"))

    def try_select(self):
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM "+self.schema_name+"."+self.schema_name+";")
            cur.execute("SELECT * FROM "+self.schema_name+"."+self.schema_name+"_softwarelist;")
            conn.close()
            return True
        except:
            conn.close()
            return True

    def post_content_relacional(self, orgao_name, headers):
        # Verifica registro por registro e adiciona o campo name_orgao
        orgao_doc_results = requests.get(config.REST_URL+"/"+orgao_name+"/doc?$$={\"limit\":50}")
        orgao_doc = json.loads(orgao_doc_results.text)
        orgao_doc = orgao_doc["results"]

        # Verifica se os databases já foram criados.
        for item in orgao_doc:
            item["name_orgao"] = orgao_name
            item.pop("_metadata", None)
            if not item["softwarelist"]:
                item.pop("softwarelist", None)
            json_data_doc = json.dumps(item)
            relacional_path = self.lbrelacional_url+"/sqlapi/lightbase/content/"+self.schema_name
            postRelacionalDoc = requests.post(relacional_path, data=json_data_doc, headers=headers)