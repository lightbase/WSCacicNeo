#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import os
import json
import requests
from requests.exceptions import HTTPError
from wscacicneo import config
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbutils.codecs import json2object
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()


class DescriptionsBase(object):
    """
    Classe para a base de atividades
    """

    def __init__(self, rest_url=None):
        """
        Método construtor da base de atividades
        :param rest_url: URL do Rest
        """
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=False)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)
        here = os.path.abspath(os.path.dirname(__file__))
        data_dir = os.path.join(here, '../data/')
        self.data_dir = data_dir

    @property
    def lbbase(self):
        """
        Base no LB
        :return: LB Base object
        """
        win32_physicalmemory_memorytype_list = Content()

        win32_physicalmemory_memorytype_key = Field(**dict(
            name='win32_physicalmemory_memorytype_key',
            description='Chave do atributo MemoryType',
            alias='win32_physicalmemory_memorytype_key',
            datatype='Integer',
            indices=['Ordenado'],
            multivalued=False,
            required=False
        ))

        win32_physicalmemory_memorytype_list.append(win32_physicalmemory_memorytype_key)

        win32_physicalmemory_memorytype_value = Field(**dict(
            name='win32_physicalmemory_memorytype_value',
            description='Valro do atributo MemoryType',
            alias='win32_physicalmemory_memorytype_value',
            datatype='Text',
            indices=['Textual', 'Ordenado'],
            multivalued=False,
            required=False
        ))

        win32_physicalmemory_memorytype_list.append(win32_physicalmemory_memorytype_value)

        win32_physicalmemory_memorytype_metadata = GroupMetadata(**dict(
            name='win32_physicalmemory_memorytype',
            alias='win32_physicalmemory_memorytype',
            description='Descrição do campo win32_physicalmemory_memorytype',
            multivalued=True
        ))

        win32_physicalmemory_memorytype = Group(
            metadata=win32_physicalmemory_memorytype_metadata,
            content=win32_physicalmemory_memorytype_list
        )

        win32_processor_family_list = Content()

        win32_processor_family_key = Field(**dict(
            name='win32_processor_family_key',
            description='Chave do atributo MemoryType',
            alias='win32_processor_family_key',
            datatype='Integer',
            indices=['Ordenado'],
            multivalued=False,
            required=False
        ))

        win32_processor_family_list.append(win32_processor_family_key)

        win32_processor_family_value = Field(**dict(
            name='win32_processor_family_value',
            description='Valor do atributo Family',
            alias='win32_processor_family_value',
            datatype='Text',
            indices=['Textual', 'Ordenado'],
            multivalued=False,
            required=False
        ))

        win32_processor_family_list.append(win32_processor_family_value)

        win32_processor_family_metadata = GroupMetadata(**dict(
            name='win32_processor_family',
            alias='win32_processor_family',
            description='Descrição do campo win32_processor_family',
            multivalued=True
        ))

        win32_processor_family = Group(
            metadata=win32_processor_family_metadata,
            content=win32_processor_family_list
        )

        content_list = Content()
        content_list.append(win32_physicalmemory_memorytype)
        content_list.append(win32_processor_family)

        base_metadata = BaseMetadata(
            name='descriptions',
            description='Field descriptions'
        )

        lbbase = Base(
            metadata=base_metadata,
            content=content_list
        )

        return lbbase

    @property
    def metaclass(self):
        """
        Retorna metaclass para essa base
        """
        return self.lbbase.metaclass()

    def create_base(self):
        """
        Cria base no LB
        """
        try:
            response = self.baserest.create(self.lbbase)
            return True
        except HTTPError:
            raise IOError('Error inserting base in LB')

    def remove_base(self):
        """
        Remove base from Lightbase
        :param lbbase: LBBase object instance
        :return: True or Error if base was not excluded
        """
        url = self.rest_url + '/' + self.lbbase.metadata.name
        response = requests.delete(url)

        #response = self.baserest.delete(self.lbbase)

        return response

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            response = self.baserest.get(self.lbbase.metadata.name)
            return True
        except HTTPError:
            return False

    def load_static(self):
        """
        Carrega valores dos grupos do arquivo JSON contido no Projeto
        :return:
        """
        # TODO: Coloca esses grupos e um valor definido pelo usuario
        groups_list = [
            'win32_physicalmemory_memorytype',
            'win32_processor_family'
        ]

        saida = dict()
        for group in groups_list:
            saida[group] = list()
            # Carrega valor do JSON para cada um ds grupos
            filename = self.data_dir + group + ".json"
            log.debug("Caminho completo do arquivo para carga: %s", filename)
            with open(filename, 'r', encoding='utf-8') as fd:
                value = json.loads(fd.read())
            #log.debug(value)
            for elm in value:
                #log.debug("111111111111111111111111111111")
                #log.debug(elm)
                # Faz o parsing do JSON por linha
                for key in elm.keys():
                    saida[group].append({
                        group + '_key': int(key),
                        group + '_value': elm[key]
                    })

        # Valida documento
        #log.debug(saida)
        document = conv.dict2document(self.lbbase, saida)
        document_json = conv.document2json(self.lbbase, document)
        log.debug(document_json)

        # FIXME: Verificar para que serve a remoção da base.
        # Recria base e insere um documento
        if self.is_created():
            self.remove_base()
        # try:
        #     self.create_base()
        # except:
        #     pass
        self.create_base()
        self.documentrest.create(document_json)

desc = DescriptionsBase()


class Desc(desc.metaclass):
    """
    Classe genérica de órgãos
    """
    def __init__(self, **args):
        super(Desc, self).__init__(**args)
        self.documentrest = desc.documentrest

    @property
    def coleta(self):
        """
        Tempo de coleta
        :return: Retorna o valor gravado ou o mínimo de 3 horas
        """
        col = desc.metaclass.coleta.__get__(self)
        if col is None:
            return 3
        else:
            return col

    @coleta.setter
    def coleta(self, value):
        """
        Setter
        """
        value = int(value)
        desc.metaclass.coleta.__set__(self, value)

    def desc_to_dict(self):
        """
        Convert status object to Python dict
        :return:
        """

        return conv.document2dict(desc.lbbase, self)

    def desc_to_json(self):
        """
        Convert object to json
        :return:
        """

        return conv.document2json(desc.lbbase, self)

    def search_desc(self, attr):
       """
       Executa uma Busca na Base
       """
       search = Search(
           select = [attr]
       )
       results = self.documentrest.get_collection(search_obj=search)

       return results

    def create_dict_to_desc(self, elm):
        """
        Cria um dict apartir de um grupo 
        """
        search = Search(
           select = [elm]
        )
        result = self.documentrest.get_collection(search_obj=search)
        dict_desc = dict()
        y = json.loads(result.results)
        for x in y.keys():
            dict_desc[x] = y[x]

        return dict_desc

