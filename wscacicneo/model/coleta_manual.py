#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'adley'

from requests.exceptions import HTTPError
from wscacicneo import config
import logging
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()

class ColetaManualBase():
    """
    Classe para a base de usuários
    """
    def __init__(self, nm_base, rest_url=None):
        """
        Método construtor
        """
        self.nm_base = nm_base
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)

    @property
    def lbbase(self):

        """
        COnfiguração da Coleta
        """
        data_coleta = Field(**dict(
            name='data_coleta',
            description='Data da Coleta',
            alias='data_coleta',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        """
        LB Processadores
        """
        nome_processador = Field(**dict(
            name='nome_processador',
            description='Nome do Processador',
            alias='nome_processador',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        versao_processador = Field(**dict(
            name='versao_processador',
            description='Versão do Processador',
            alias='versao_processaodr',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        
        data_instalacao_processador = Field(**dict(
            name='data_instalacao_processador',
            description='Data da Instalação do Processador',
            alias='data_instalacao_processaodr',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        """
        LB HD
        """
        marca_hd = Field(**dict(
            name='marca_hd',
            description='Marca do HD',
            alias='marca_hd',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        tamanho_hd = Field(**dict(
            name='tamanho_hd',
            description='Tamanho do HD',
            alias='tamanho_hd',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        tipo_hd = Field(**dict(
            name='tipo_hd',
            description='Tipo do HD',
            alias='tipo_hd',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        idade_hd = Field(**dict(
            name='idade_hd',
            description='Idade do HD',
            alias='idade_hd',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        
        """
        LB Memória
        """

        interface_memoria = Field(**dict(
            name='interface_memoria',
            description='Interface da Memória',
            alias='interface_memoria',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        armazenamento_memoria = Field(**dict(
            name='armazenamento_memoria',
            description='Armazenamento da Memória',
            alias='armazenamento_memoria',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        idade_memoria = Field(**dict(
            name='idade_memoria',
            description='Idade do Memória',
            alias='idade_memoria',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        """
        LB Sistema Operacional
        """
        nome_so = Field(**dict(
            name='nome_so',
            description='Nome do Sistema Operacional',
            alias='nome_so',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        versao_so = Field(**dict(
            name='versao_so',
            description='Versão do Sistema Operacional',
            alias='versao_so',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        fabricante_so = Field(**dict(
            name='fabricante_so',
            description='Fabricando do Sistema Operacional',
            alias='fabricante_so',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        """
        LB Bios
        """
        patrimonio_bios = Field(**dict(
            name='patrimonio_bios',
            description='Patrimonio da Bios',
            alias='patrimonio_bios',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))
        fabricante_bios = Field(**dict(
            name='fabricante_bios',
            description='Fabricante da Bios',
            alias='fabricante_bios',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        """
        GROUP Sistema Operacional
        """
        sistemaoperacional_content = Content()
        sistemaoperacional_content.append(nome_so)
        sistemaoperacional_content.append(versao_so)
        sistemaoperacional_content.append(fabricante_so)

        sistemaoperacional_metadata = GroupMetadata(
            name='sistemaoperacional',
            alias='sistemaoperacional',
            description='Sistema Operacional',
            multivalued = False
        )

        sistemaoperacional = Group(
            metadata = sistemaoperacional_metadata,
            content = sistemaoperacional_content
        )

        """
        GROUP Bios
        """
        bios_content = Content()
        bios_content.append(patrimonio_bios)
        bios_content.append(fabricante_bios)

        bios_metadata = GroupMetadata(
            name='bios',
            alias='bios',
            description='Bios',
            multivalued = False
        )

        bios = Group(
            metadata = bios_metadata,
            content = bios_content
        )

        """
        GROUP Memória
        """
        memoria_content = Content()
        memoria_content.append(interface_memoria)
        memoria_content.append(armazenamento_memoria)
        memoria_content.append(idade_memoria)

        memoria_metadata = GroupMetadata(
            name='memoria',
            alias='memoria',
            description='Memória',
            multivalued = False
        )

        memoria = Group(
            metadata = memoria_metadata,
            content = memoria_content
        )

        """
        GROUP HD
        """
        hd_content = Content()
        hd_content.append(marca_hd)
        hd_content.append(tamanho_hd)
        hd_content.append(tipo_hd)
        hd_content.append(idade_hd)

        hd_metadata = GroupMetadata(
            name='hd',
            alias='hd',
            description='HD',
            multivalued = False
        )

        hd = Group(
            metadata = hd_metadata,
            content = hd_content
        )

        """
        GROUP Processador
        """
        processador_content = Content()
        processador_content.append(nome_processador)
        processador_content.append(versao_processador)
        processador_content.append(data_instalacao_processador)

        processador_metadata = GroupMetadata(
            name='processador',
            alias='processador',
            description='Processador',
            multivalued = False
        )

        processador = Group(
            metadata = processador_metadata,
            content = processador_content
        )

        base_metadata = BaseMetadata(
            name = self.nm_base,
        )

        content_list = Content()
        content_list.append(data_coleta)
        content_list.append(processador)
        content_list.append(hd)
        content_list.append(bios)
        content_list.append(memoria)
        content_list.append(sistemaoperacional)

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
        response = self.baserest.create(self.lbbase)
        if response.status_code == 200:
            return self.lbbase
        else:
            return None

    def remove_base(self):
        """
        Remove base from Lightbase
        :param lbbase: LBBase object instance
        :return: True or Error if base was not excluded
        """
        response = self.baserest.delete(self.lbbase)
        if response.status_code == 200:
            return True
        else:
            raise IOError('Error excluding base from LB')
