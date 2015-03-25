#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc



def dict_desc():
    dict_desc = {
        0 : 'Unknown',
        1 : 'Other',
        2 : 'DRAM',
        3 : 'Synchronous DRAM',
        4 : 'Cache DRAM',
        5 : 'EDO',
        6 : 'EDRAM',
        7 : 'VRAM',
        8 : 'SRAM',
        9 : 'RAM',
        10 : 'ROM',
        11 : 'Flash',
        12 : 'EEPROM',
        13 : 'FEPROM',
        14 : 'EPROM',
        15 : 'CDRAM',
        16 : '3DRAM',
        17 : 'SDRAM',
        18 : 'RDRAM',
        19 : 'DDR',
        21 : 'DDR-2',
    }

    return dict_desc
