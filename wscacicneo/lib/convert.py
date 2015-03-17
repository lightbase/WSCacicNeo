#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc




def conv_to_dict(saida, elm):
    """
    Converte os dados do dicionario
    """
    dict_to_desc = Desc.create_dict_to_desc(elm)
    dict_to_saida = dict()
    for x in dict_saida.keys():
        dict_to_saida[dict_to_desc[x]] = dict_saida[x]

    return dict_to_saida
