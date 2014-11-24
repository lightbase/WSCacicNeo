#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

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

class ReportsBase():
    """
    Classe para a base de Reports
    """
    def __init__(self, nm_base,rest_url=None):
        """
        Método construtor
        """
        self.nm_base = nm_base
        if rest_url is None:
            self.rest_url= config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)

    @property
    def lbbase(self):
        """
        LB Base do órgão
        """
        OperatingSystem_item = Field(**dict(
            name='OperatingSystem_item',
            description='Item Coletado',
            alias='Item',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=True
        ))

        OperatingSystem_amount = Field(**dict(
            name='OperatingSystem_amount',
            alias='amount',
            description='amount',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        Win32_BIOS_item = Field(**dict(
            name='Win32_BIOS_item',
            description='Item Coletado',
            alias='Item',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=True
        ))

        Win32_BIOS_amount = Field(**dict(
            name='Win32_BIOS_amount',
            alias='amount',
            description='amount',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        Win32_Processor_item = Field(**dict(
            name='Win32_Processor_item',
            description='Item Coletado',
            alias='Item',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=True
        ))

        Win32_Processor_amount = Field(**dict(
            name='Win32_Processor_amount',
            alias='amount',
            description='amount',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        Win32_LogicalDisk_item = Field(**dict(
            name='Win32_LogicalDisk_item',
            description='Item Coletado',
            alias='Item',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=True
        ))

        Win32_LogicalDisk_amount = Field(**dict(
            name='Win32_LogicalDisk_amount',
            alias='amount',
            description='amount',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        Win32_PhysicalMemory_item = Field(**dict(
            name='Win32_PhysicalMemory_item',
            description='Item Coletado',
            alias='Item',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=True
        ))

        Win32_PhysicalMemory_amount = Field(**dict(
            name='Win32_PhysicalMemory_amount',
            alias='amount',
            description='amount',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        """
        GROUP Sistema Operacional
        """
        OperatingSystem_content = Content()
        OperatingSystem_content.append(OperatingSystem_item)
        OperatingSystem_content.append(OperatingSystem_amount)

        OperatingSystem_metadata = GroupMetadata(
            name='OperatingSystem',
            alias='OperatingSystem',
            description='OperatingSystem',
            multivalued = False
        )

        OperatingSystem = Group(
            metadata = OperatingSystem_metadata,
            content = OperatingSystem_content
        )

        """
        GROUP Bios
        """
        Win32_BIOS_content = Content()
        Win32_BIOS_content.append(Win32_BIOS_item)
        Win32_BIOS_content.append(Win32_BIOS_amount)

        Win32_BIOS_metadata = GroupMetadata(
            name='Win32_BIOS',
            alias='Win32_BIOS',
            description='Win32_BIOS',
            multivalued = False
        )

        Win32_BIOS = Group(
            metadata = Win32_BIOS_metadata,
            content = Win32_BIOS_content
        )

        """
        GROUP Processador
        """
        Win32_Processor_content = Content()
        Win32_Processor_content.append(Win32_Processor_item)
        Win32_Processor_content.append(Win32_Processor_amount)

        Win32_Processor_metadata = GroupMetadata(
            name='Win32_Processor',
            alias='Win32_Processor',
            description='Win32_Processor',
            multivalued = False
        )

        Win32_Processor = Group(
            metadata = Win32_Processor_metadata,
            content = Win32_Processor_content
        )

        """
        GROUP LogicalDisk
        """
        Win32_LogicalDisk_content = Content()
        Win32_LogicalDisk_content.append(Win32_LogicalDisk_item)
        Win32_LogicalDisk_content.append(Win32_LogicalDisk_amount)

        Win32_LogicalDisk_metadata = GroupMetadata(
            name='Win32_LogicalDisk',
            alias='Win32_LogicalDisk',
            description='Win32_LogicalDisk',
            multivalued = False
        )

        Win32_LogicalDisk = Group(
            metadata = Win32_LogicalDisk_metadata,
            content = Win32_LogicalDisk_content
        )

        """
        GROUP PhysicalMemory
        """
        Win32_PhysicalMemory_content = Content()
        Win32_PhysicalMemory_content.append(Win32_PhysicalMemory_item)
        Win32_PhysicalMemory_content.append(Win32_PhysicalMemory_amount)

        Win32_PhysicalMemory_metadata = GroupMetadata(
            name='Win32_PhysicalMemory',
            alias='Win32_PhysicalMemory',
            description='Win32_PhysicalMemory',
            multivalued = False
        )

        Win32_PhysicalMemory = Group(
            metadata = Win32_PhysicalMemory_metadata,
            content =  Win32_PhysicalMemory_content
        )

        base_metadata = BaseMetadata(
            name = self.nm_base + "_bk",
        )

        content_list = Content()
        content_list.append(OperatingSystem)
        content_list.append(Win32_BIOS)
        content_list.append(Win32_Processor)
        content_list.append(Win32_PhysicalMemory)
        content_list.append(Win32_LogicalDisk)

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
        self.baserest.response_object = True
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

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            self.baserest.response_object = False
            response = self.baserest.get(self.lbbase.metadata.name)
            self.baserest.response_object = True
            return True
        except:
            return False

