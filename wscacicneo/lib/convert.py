#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

import json
import os
import logging
from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc

log = logging.getLogger()


def dict_desc(group):
    here = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(here, '../data/')
    filename = data_dir + group + ".json"

    with open(filename, 'r', encoding='utf-8') as fd:
        value = json.loads(fd.read())

    saida = dict()
    for elm in value:
        # Faz o parsing do JSON por linha
        for key in elm.keys():
            saida[int(key)] = elm[key]

    return saida
