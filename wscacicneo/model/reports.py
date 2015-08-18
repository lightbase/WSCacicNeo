#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

from requests.exceptions import HTTPError
from wscacicneo import config
import logging
import os
import json
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from wscacicneo.model import coleta_manual
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy
from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc
from wscacicneo.lib import convert


log = logging.getLogger()


class Reports():

    def __init__(self, nm_base, rest_url=None, response_object=True):
        self.base_nm = nm_base
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.coleta_manual_base = coleta_manual.ColetaManualBase(nm_base, self.rest_url)
        self.base = self.coleta_manual_base.lbbase
        self.documentrest = DocumentREST(self.rest_url, self.base, response_object)

    def get_base_orgao(self):
        """
        Retorna todos os documentos da base
        """
        # A resposta nao pode ser object aqui
        self.documentrest.response_object = False
        search = Search(
            limit=None
        )
        get = self.documentrest.get_collection(search_obj=search)

        return get

    def coleta_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(self.base, self)

    def coleta_to_json(self, document):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(document.lbbase, self)

    def create_coleta(self, document):
        """
        Insere dados de coleta
        """
        result = self.documentrest.create(document)
        return result
  
    def update_coleta(self, id, document):
        """
        Altera dados de coleta
        """
        coleta = self.documentrest.update(id, document)
        return coleta

    def delete_coleta(self, id, document):
        """
        Apaga os dados de coleta
        """
        coleta = self.documentrest.update(id)
        return coleta

    def get_attribute(self, attr):
        """
        Testa recuperar atributo do Documento
        """
        # A resposta nao pode ser object aqui
        self.documentrest.response_object = False

        # FIXME: Adicionar lista de atributos obrigatórios nos campos que vao retornar na busca
        # Referência: http://dev.lightbase.cc/projects/liblightbase/repository/revisions/master/entry/liblightbase/lbbase/content.py#L34

        # A busca deve obrigatoriamente retornar todos os atributos obrigatórios
        search = Search(
            limit=None,
            select=[attr, "data_coleta"]
        )
        get = self.documentrest.get_collection(search_obj=search)

        return get

    def count_attribute(self, attr, child=None):
        """
        retorna dicionário de atributos agrupados por contador
        """
        release_expressions = [ # para uso em agrupamento
            "Professional",
            "Ultimate",
            "Standard",
            "Enterprise",
            "Premium",
            "Starter",
            "MUI"
        ]
        # FIXME: Pegar um filtro mais dinâmico de offices a excluir
        excluir = [
            "Security Update".lower(),
            "Atualiza".lower(),
            "Help Pack".lower(),
            "Compatibility".lower(),
            "Definition Update".lower(),
            "Disco".lower(),
            "UNO runtime".lower(),
            "Office Access Runtime".lower(),
            "Office com Clique para Executar".lower(),
            "Components".lower(),
            "Update for".lower(),
            "Hotfix for".lower(),
            "Web Components".lower(),
            "Service Pack".lower(),
            "File Validation Add-In".lower(),
            "Office InfoPath".lower(),
            "Office Outlook Connector".lower(),
            "Office Proofing Tools".lower(),
            "Office Shared".lower(),
            "Pacote de Compatibilidade".lower(),
            "Office Groove".lower(),
            "Office OneNote".lower()
        ]

        attr_dict = self.get_attribute(attr)
        results = attr_dict.results
        # log.debug(results)
        saida = dict()
        for elm in results:
            if child:
                parent = getattr(elm, attr)
                # Verifica valores nulos
                try:
                    attribute = getattr(parent, child)
                except AttributeError:
                    continue
            else:
                attribute = getattr(elm, attr)

            if attr == 'softwarelist':
                for software in attribute:
                    # ignorar updates e atualizações
                    pula = False
                    agrupa = False
                    expressao_atual = ''
                    for ignora in excluir:
                        if software.lower().find(ignora) > -1:
                            # Se chegou aqui esse software deve ser excluído
                            pula = True
                            break

                    #atualizando expressão de agrupamento
                    expressao_atual = software
                    agrupa = False
                    if expressao_atual.lower().find('(') > 0:
                        expressao_atual = expressao_atual.split('(',1)[0] + \
                                          expressao_atual.split(')')[-1]
                        agrupa = True
                    if expressao_atual.lower().find('.') > 0:
                        expressao_atual = expressao_atual.split('.',1)[0]
                        agrupa = True
                    if expressao_atual.lower().find('-') > 0:
                        expressao_atual = expressao_atual.split('-',1)[0]
                        agrupa = True
                    if software.lower().find('20') > -1:
                        expressao_atual = expressao_atual.translate(
                            str.maketrans('','','1234567890'))
                        agrupa = True
                    # Verifica se existe alguma expressão de release
                    for release_expression in release_expressions:
                        if expressao_atual.lower().find(
                                release_expression.lower()) > 0:
                            expressao_atual = expressao_atual.split(
                                release_expression,1)[0]
                            agrupa = True
                    # Se 'pula' for verdadeiro, o software deve ser ignorado
                    if pula:
                        continue
                    # Se 'agrupa' for verdadeiro, o software será agrupado
                    if agrupa:
                        expressao_atual = expressao_atual.strip()
                        if saida.get(expressao_atual) is None:
                            saida[expressao_atual] = 1
                        else:
                            saida[expressao_atual] += 1
                        continue
                    if saida.get(software) is None:
                        saida[software] = 1
                    else:
                        saida[software] += 1
                # Criando arquivo 'software_list.json' para uso em testes
                here = os.path.abspath(os.path.dirname(__file__))
                data_path = os.path.join(here, "../test/fixtures/reports/")
                software_list_file = open(data_path + "software_list.json",
                                          "w+")
                software_list_file.write(json.dumps(saida))
            elif saida.get(attribute):
                saida[attribute] = saida.get(attribute) + 1
            else:
                saida[attribute] = 1

        if attr == 'win32_physicalmemory':
            elm = 'win32_physicalmemory_memorytype'
            saida_dict = convert.dict_desc(elm)
            dict_saida = dict()
            for x in saida.keys():
                dict_saida[saida_dict[x]] = saida[x]

            return dict_saida
        else:
            log.info(saida)
            return saida
