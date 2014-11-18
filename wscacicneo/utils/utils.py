#!/usr/env python
# -*- coding: utf-8 -*-
import requests
import json
import unicodedata
import hashlib
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase

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
        
    # Retorna um hex de um objeto hash, com uma senha encryptada
    def hash_password(password):
        hash_object = hashlib.md5(password.encode("utf-8"))
        return hash_object.hexdigest()

    def create_user_obj():
        user_obj = User(
            nome = 'usuario',
            matricula = '000000',
            email = 'usuario@gov.br',
            orgao = 'mpog',
            telefone = '(11)1111-1111',
            cargo = 'adm',
            setor = 'ti',
            permissao = 'Administrador',
            senha = '123',
            favoritos = ['favoritos'],
            itens = ['itens']
        )
        return user_obj
        
    def retorna_usuario_autenticado(email=None,matricula=None):
        if ( (email is None) and (matricula is None) ):
            return None
        elif (matricula is None):
            user_obj = Utils.create_user_obj()
            usuario = user_obj.search_user_by_email(email)
            return usuario
        else:
            user_obj = Utils.create_user_obj()
            usuario = user_obj.search_user(matricula)
            return usuario

    def create_orgao_obj():
        orgao_obj = Orgao(
            nome = 'Orgao',
            cargo = 'Cargo',
            coleta = 'Coleta',
            sigla = 'MPOG',
            endereco = 'Esplanada bloco C',
            email = 'admin@planemaneto.gov.br',
            telefone = '(61) 2025-4117',
            url = 'http://api.brlight.net/api',
        )
        return user_obj