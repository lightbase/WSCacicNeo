#!/usr/env python
# -*- coding: utf-8 -*-
import requests
import json
import unicodedata
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase


class Utils:

    def __init__(self):
        pass

    def to_url(*args):
        return '/'.join(list(args))

    # Retorna verdadeiro para um email passado no qual contenha um e-mail institucional
    # no caso, quando o e-mail tiver gov.br
    def verifica_email_institucional(email):
    	if("gov.br" in email):
    		return True
    	else:
    		return False

    # Retorna uma string sem caracteres especiais(sem espaço e acentos).
    def format_name(data):
	    return ''.join(x for x in unicodedata.normalize('NFKD', data) if \
	    unicodedata.category(x)[0] == 'L').lower()
