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


class ColetaManualBase(object):
    """
    Classe para a base de usuários
    """
    def __init__(self, nm_base, rest_url=None):
        """
        Método construtor
        """
        #print(rest_url)
        self.nm_base = nm_base
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=False)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)

    @property
    def lbbase(self):

        """
        Configuração da Coleta
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

        hash_machine = Field(**dict(
            name='hash_machine',
            description='hash para maquinas',
            alias='hash_machine',
            datatype='Text',
            indices=['Textual', 'Unico'],
            multivalued=False,
            required=False
        ))

        data_ultimo_acesso = Field(**dict(
            name='data_ultimo_acesso',
            description='data do ultimo acesso',
            alias='data acesso',
            datatype='DateTime',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        # Adições Jansen: 2015-11-26
        mac = Field(**dict(
            name='mac',
            description='MAC Address',
            alias='MAC',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        ip_computador = Field(**dict(
            name='ip_computador',
            description='IP do Computador',
            alias='Endereço IP',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        ip_rede = Field(**dict(
            name='ip_rede',
            description='IP da Rede',
            alias='IP da Rede',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        nome_rede = Field(**dict(
            name='nome_rede',
            description='Nome da Rede',
            alias='Nome da Rede',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        """
        LB Processadores
        """
        Win32_Processor_Manufacturer = Field(**dict(
            name='Win32_Processor_Manufacturer',
            description='Win32_Processor_Manufacturer',
            alias='Win32_Processor_Manufacturer',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        Win32_Processor_NumberOfLogicalProcessors = Field(**dict(
            name='Win32_Processor_NumberOfLogicalProcessors',
            description='Win32_Processor_NumberOfLogicalProcessors',
            alias='Win32_Processor_NumberOfLogicalProcessors',
            datatype='Integer',
            indices=[],
            multivalued=False,
            required=False
        ))

        Win32_Processor_Caption = Field(**dict(
            name='Win32_Processor_Caption',
            description='Win32_Processor_Caption',
            alias='Win32_Processor_Caption',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        Win32_Processor_MaxClockSpeed = Field(**dict(
            name='Win32_Processor_MaxClockSpeed',
            description='Win32_Processor_MaxClockSpeed',
            alias='Win32_Processor_MaxClockSpeed',
            datatype='Integer',
            indices=[],
            multivalued=False,
            required=False
        ))

        Win32_Processor_Family = Field(**dict(
            name='Win32_Processor_Family',
            description='Win32_Processor_Family',
            alias='Win32_Processor_Family',
            datatype='Integer',
            indices=[],
            multivalued=False,
            required=False
        ))

        # Adições Jansen: 2015-11-26
        win32_processor_installdate = Field(**dict(
            name='win32_processor_installdate',
            description='win32_processor_installdate',
            alias='win32_processor_installdate',
            datatype='Text',
            indices=[],
            multivalued=False,
            required=False
        ))

        """
        BaseBoard
        """
        # Adições Jansen: 2015-11-26
        win32_baseboard_installdate = Field(**dict(
            name='win32_baseboard_installdate',
            description='win32_baseboard_installdate',
            alias='win32_baseboard_installdate',
            datatype='Text',
            indices=[],
            multivalued=False,
            required=False
        ))

        """
        LB Sistema Operacional
        """
        OperatingSystem_Version = Field(**dict(
            name='OperatingSystem_Version',
            description='OperatingSystem_Version',
            alias='OperatingSystem_Version',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        OperatingSystem_InstallDate = Field(**dict(
            name='OperatingSystem_InstallDate',
            description='OperatingSystem_InstallDate',
            alias='OperatingSystem_InstallDate',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        OperatingSystem_Caption = Field(**dict(
            name='OperatingSystem_Caption',
            description='OperatingSystem_Caption',
            alias='OperatingSystem_Caption',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        """
        LB SoftwareList
        """
        SoftwareList = Field(**dict(
            name='SoftwareList',
            description='SoftwareList',
            alias='SoftwareList',
            datatype='Text',
            indices=['Textual'],
            multivalued=True,
            required=False
        ))

        """
        LB Bios
        """
        Win32_BIOS_Manufacturer = Field(**dict(
            name='Win32_BIOS_Manufacturer',
            description='Win32_BIOS_Manufacturer',
            alias='Win32_BIOS_Manufacturer',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        # Adições Jansen: 2015-11-26
        win32_bios_installdate = Field(**dict(
            name='win32_bios_installdate',
            description='win32_bios_installdate',
            alias='win32_bios_installdate',
            datatype='Text',
            indices=[],
            multivalued=False,
            required=False
        ))

        win32_bios_releasedate = Field(**dict(
            name='win32_bios_releasedate',
            description='win32_bios_releasedate',
            alias='win32_bios_releasedate',
            datatype='Text',
            indices=[],
            multivalued=False,
            required=False
        ))

        """
        LB Physical Memory
        """
        Win32_PhysicalMemory_MemoryType = Field(**dict(
            name='Win32_PhysicalMemory_MemoryType',
            description='Win32_PhysicalMemory_MemoryType',
            alias='Win32_PhysicalMemory_MemoryType',
            datatype='Integer',
            indices=[],
            multivalued=False,
            required=False
        ))

        Win32_PhysicalMemory_Capacity = Field(**dict(
            name='Win32_PhysicalMemory_Capacity',
            description='Win32_PhysicalMemory_Capacity',
            alias='Win32_PhysicalMemory_Capacity',
            datatype='Integer',
            indices=[],
            multivalued=False,
            required=False
        ))

        """
        LB Disk
        """
        Win32_DiskDrive_Caption = Field(**dict(
            name='Win32_DiskDrive_Caption',
            description='Win32_DiskDrive_Caption',
            alias='Win32_DiskDrive_Caption',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        Win32_DiskDrive_Model = Field(**dict(
            name='Win32_DiskDrive_Model',
            description='Win32_DiskDrive_Model',
            alias='Win32_DiskDrive_Model',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        Win32_DiskDrive_Size = Field(**dict(
            name='Win32_DiskDrive_Size',
            description='Win32_DiskDrive_Size',
            alias='Win32_DiskDrive_Size',
            datatype='Integer',
            indices=[],
            multivalued=False,
            required=False
        ))

        """
        GROUP Sistema Operacional
        """
        OperatingSystem_content = Content()
        OperatingSystem_content.append(OperatingSystem_Version)
        OperatingSystem_content.append(OperatingSystem_InstallDate)
        OperatingSystem_content.append(OperatingSystem_Caption)

        OperatingSystem_metadata = GroupMetadata(
            name='OperatingSystem',
            alias='OperatingSystem',
            description='OperatingSystem',
            multivalued=False
        )

        OperatingSystem = Group(
            metadata=OperatingSystem_metadata,
            content=OperatingSystem_content
        )

        """
        GROUP Bios
        """
        Win32_BIOS_content = Content()
        Win32_BIOS_content.append(Win32_BIOS_Manufacturer)
        Win32_BIOS_content.append(win32_bios_installdate)
        Win32_BIOS_content.append(win32_bios_releasedate)

        Win32_BIOS_metadata = GroupMetadata(
            name='Win32_BIOS',
            alias='Win32_BIOS',
            description='Win32_BIOS',
            multivalued=False
        )

        Win32_BIOS = Group(
            metadata = Win32_BIOS_metadata,
            content = Win32_BIOS_content
        )

        """
        GROUP Processador
        """
        Win32_Processor_content = Content()
        Win32_Processor_content.append(Win32_Processor_Manufacturer)
        Win32_Processor_content.append(Win32_Processor_NumberOfLogicalProcessors)
        Win32_Processor_content.append(Win32_Processor_Caption)
        Win32_Processor_content.append(Win32_Processor_MaxClockSpeed)
        Win32_Processor_content.append(Win32_Processor_Family)
        Win32_Processor_content.append(win32_processor_installdate)

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
        GROUP Physical Memory
        """
        Win32_PhysicalMemory_content = Content()
        Win32_PhysicalMemory_content.append(Win32_PhysicalMemory_Capacity)
        Win32_PhysicalMemory_content.append(Win32_PhysicalMemory_MemoryType)

        Win32_PhysicalMemory_metadata = GroupMetadata(
            name='Win32_PhysicalMemory',
            alias='Win32_PhysicalMemory',
            description='Win32_PhysicalMemory',
            multivalued=False
        )

        Win32_PhysicalMemory = Group(
            metadata=Win32_PhysicalMemory_metadata,
            content=Win32_PhysicalMemory_content
        )

        """
        GROUP Logical Disk
        """
        Win32_DiskDrive_content = Content()
        Win32_DiskDrive_content.append(Win32_DiskDrive_Caption)
        Win32_DiskDrive_content.append(Win32_DiskDrive_Model)
        Win32_DiskDrive_content.append(Win32_DiskDrive_Size)

        Win32_DiskDrive_metadata = GroupMetadata(
            name='Win32_DiskDrive',
            alias='Win32_DiskDrive',
            description='Win32_DiskDrive',
            multivalued=False
        )

        Win32_DiskDrive = Group(
            metadata=Win32_DiskDrive_metadata,
            content=Win32_DiskDrive_content
        )

        """
        Group BaseBoard
        """
        Win32_BaseBoard_content = Content()
        Win32_BaseBoard_content.append(win32_baseboard_installdate)

        Win32_BaseBoard_metadata = GroupMetadata(
            name='Win32_BaseBoard',
            alias='Win32_BaseBoard',
            description='Win32_BaseBoard',
            multivalued=False
        )

        Win32_BaseBoard = Group(
            metadata=Win32_BaseBoard_metadata,
            content=Win32_BaseBoard_content
        )


        base_metadata = BaseMetadata(
            name=self.nm_base,
        )

        content_list = Content()
        content_list.append(data_coleta)
        content_list.append(Win32_Processor)
        content_list.append(OperatingSystem)
        content_list.append(Win32_BIOS)
        content_list.append(Win32_PhysicalMemory)
        content_list.append(Win32_DiskDrive)
        content_list.append(Win32_BaseBoard)
        content_list.append(SoftwareList)
        content_list.append(hash_machine)
        content_list.append(data_ultimo_acesso)
        content_list.append(mac)
        content_list.append(ip_computador)
        content_list.append(ip_rede)
        content_list.append(nome_rede)

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
        try:
            response = self.baserest.delete(self.lbbase)
            return True
        except HTTPError:
            raise IOError('Error excluding base from LB')

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            response = self.baserest.get(self.lbbase.metadata.name)
            return True
        except HTTPError:
            return False

    def update_base(self):
        """
        Remove base from Lightbase
        :param lbbase: LBBase object instance
        :return: True or Error if base was not excluded
        """
        try:
            response = self.baserest.update(self.lbbase)
            return True
        except HTTPError:
            raise IOError('Error updating base in LB')
