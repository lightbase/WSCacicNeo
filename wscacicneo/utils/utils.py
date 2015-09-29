#!/usr/env python
# -*- coding: utf-8 -*-
import requests
import string
import random
import json
import datetime
import unicodedata
import hashlib
import logging
from requests.exceptions import HTTPError
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase
from wscacicneo.model.base_reports import ReportsBase
from wscacicneo.model.config_reports import ConfReports
from wscacicneo.model.coleta_manual import ColetaManualBase
from wscacicneo.model.reports import Reports
from wscacicneo.model.atividade import Atividade
from wscacicneo.model.atividade import AtividadeBase
from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc
from wscacicneo import config
from wscacicneo.model import blacklist


log = logging.getLogger()


class Utils:

    def __init__(self):
        pass

    def dict_depth(d, depth=0):
        if not isinstance(d, dict) or not d:
            return depth
        return max(Utils.dict_depth(v, depth+1) for k, v in d.items())

    def to_url(*args):
        return '/'.join(list(args))

    # Retorna verdadeiro para um email passado no qual contenha um e-mail institucional
    # no caso, quando o e-mail tiver gov.br
    def verifica_email_institucional(email):
        if "gov.br" in email:
            return True
        else:
            return False

    # Retorna uma string sem caracteres especiais(sem espaço e acentos).
    def format_name(data):
        return ''.join(x for x in unicodedata.normalize('NFKD', data) if \
                       unicodedata.category(x)[0] == 'L').lower()

    # Retorna um hex de um objeto hash, com uma senha encryptada
    def hash_password(password):
        hash_object = hashlib.sha512(password.encode("utf-8"))
        return hash_object.hexdigest()

    def hash_name_by_user(nm_user):
        hash_object = hashlib.sha512(nm_user.encode("utf-8"))
        return hash_object.hexdigest()


    def create_user_obj():
        user_obj = User(
            nome = 'usuario',
            pretty_name='wfçdfdsçv',
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

    def retorna_usuario_autenticado(user_id=None, matricula=None):
        # Retorna o usuário atual autenticado no sistema
        if user_id is None and matricula is None:
            return None
        elif matricula is None:
            user_obj = Utils.create_user_obj()
            usuario = user_obj.get_user_by_id(user_id)
            return usuario
        else:
            user_obj = Utils.create_user_obj()
            usuario = user_obj.search_user(matricula)
            return usuario

    def create_orgao_obj():
        orgao_obj = Orgao(
            nome='Orgao',
            pretty_name='wfçdfdsçv',
            cargo='Cargo',
            coleta=60,
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117',
            url='http://api.brlight.net/api',
            api_key='123',
            gestor='gestor'
        )
        return orgao_obj

    def return_all_bases_list():
        # RETORNA TODAS AS BASES
        bases = requests.get(config.REST_URL+'?$$={"limit":null}')
        bases_dict = bases.json()
        base_list = []
        for value in bases_dict["results"]:
            base_list.append(value["metadata"]["name"])
        return base_list

    def return_base_by_name(base_name):
        # RETORNA BASE ESPECÍFICA
        base_doc = requests.get(config.REST_URL+'/'+base_name+'/doc')
        base_dict = base_doc.json()
        return base_dict

    def is_base_coleta(base_obj):
        try:
            search_in_doc = base_obj["results"][0]["win32_bios"]
            return True
        except:
            return False

    def descriptions(self, item):
        """
        Adiciona descrição para os campos.
        """
        desc = Desc()
        search = desc.search_desc(item)
        saida = dict()
        for elm in search.keys():
            saida[elm] = search[elm]

        return saida

    def computers_not_found(data, total):
        count_items = 0

        for key in data.keys():
            if not isinstance(data[key], type(dict())):
                count_items = count_items + data[key]
            else:
                for item_amount in data[key].keys():
                    count_items = count_items + data[key][item_amount]
        if count_items < total:
            count_final = total - count_items
            data['Não Informados'] = count_final
        return data

    def return_blacklist(self):
        blacklist_obj = blacklist.Blacklist(item="name")
        search_blacklist = blacklist_obj.search_list_items()
        blacklist_result = search_blacklist.results
        list_items = []
        for elm in blacklist_result:
            list_items.append(elm.item)
        return list_items

    def create_report(self, nm_base):
        """
        Inseri Relatorio completo na base de relatorios
        """
        base_reports = ReportsBase(nm_base)
        reports_conf = ConfReports(nm_base)
        coleta_base = ColetaManualBase(nm_base)
        report = Reports(nm_base)
        itens = {
            "win32_processor": "win32_processor_manufacturer",
            "win32_bios": "win32_bios_manufacturer",
            "operatingsystem": "operatingsystem_caption",
            "win32_diskdrive": "win32_diskdrive_caption",
            "win32_physicalmemory": "win32_physicalmemory_memorytype",
            "softwarelist": None
        }
        blacklist_obj = blacklist.Blacklist(item="name")
        search_blacklist = blacklist_obj.search_list_items()
        blacklist_result = search_blacklist.results
        in_blacklist = False
        #try:
        for elm in itens.keys():
            attr = elm
            child = itens[elm]
            data = report.count_attribute(attr, child)
            for element in data:
                if str(element).strip() == '':
                    log.error("Elemento nulo enviado: %s", elm)
                    continue
                # Verifica se os itens do relatório estão presentes na blacklist
                for elm_blacklist in blacklist_result:
                    if elm_blacklist.item == element:
                        print("black=",elm_blacklist.item)
                        print("elemento=",element)
                        print(elm_blacklist == element)
                    if elm_blacklist.item == element:
                        in_blacklist = True
                        break
                if in_blacklist:
                    in_blacklist = False
                    continue
                else:
                    data_json = {
                        attr: {
                            attr+'_item': str(element),
                            attr+'_amount': int(data[element])
                        }
                    }
                    document = json.dumps(data_json)
                    try:
                        reports_conf.create_coleta(document)
                    except HTTPError as e:
                        log.error("Erro na inserção do documento\n%s", e.strerror)
        return 1
        #except:
        #return 0

    @staticmethod
    def create_atividade_obj():
        atividade_obj = Atividade(
            tipo='atividade',
            usuario='José',
            descricao='breve descrição',
            data='22/03/2014'
        )
        return atividade_obj

    def check_has_user():
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        result_count = search.result_count
        return result_count > 0

    def check_has_orgao():
        orgao_obj = Utils.create_orgao_obj()
        search = orgao_obj.search_list_orgaos()
        result_count = search.result_count
        return result_count > 0


    def check_valid_hash(self, data_hash, expire_day):
        """
        Valida o data do hash do usuario
        """
        date_today = datetime.datetime.now()
        data_hash_now = date_today.day
        valid_result = abs(data_hash_now - data_hash)
        if valid_result >= expire_day:
            return False
        else:
            return True

    def random_hash(self, hash_size):
        """
        Criar um hash aleatoriamente
        """
        hash_random = random.getrandbits(hash_size)

        return hash_random

    def verifica_orgaos(orgao):
        list_id_users = []
        user_obj = Utils.create_user_obj()
        users = user_obj.search_list_users()
        for x in range(users.result_count):
            user_orgao = users.results[x].orgao
            if user_orgao == orgao:
                list_id_users.append(users.results[x]._metadata.id_doc)
        return list_id_users

    def verifica_admin(list_users):
        user_obj = Utils.create_user_obj()
        list_admins = []
        for x in list_users:
            usuario = user_obj.get_user_by_id(x)
            if usuario.permissao == "Administrador":
                list_admins.append(usuario)
        return list_admins

    def getMaxOfList(list):
        return max(list)

    def remove_usuario(list_users):

        return True

    def convert_to_index(saida):
        for x in saida.keys():
            x = int(saida[x])

        return saida

    def random_string(length):
            rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
            return rand_string

    def group_data(ungrouped_data):

        release_expressions = [ # para uso em agrupamento
            "Professional",
            "Ultimate",
            "Standard",
            "Enterprise",
            "Premium",
            "Starter",
            "MUI"
        ]
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
        saida = dict()
        for software in ungrouped_data.keys():
            agrupa = False
            pula=False
            expressao_atual=software
            for ignora in excluir:
                if expressao_atual.lower().find(ignora) > -1:
                    # Se chegou aqui esse software deve ser excluído
                    pula = True
                    break
            # Se 'pula' for verdadeiro, o software deve ser ignorado
            if pula:
                continue
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
            if expressao_atual.lower().find('20') > -1:
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
            if agrupa:
                expressao_atual = expressao_atual.strip()
                if saida.get(expressao_atual) is None:
                    saida[expressao_atual] = ungrouped_data[software]
                else:
                    saida[expressao_atual] += ungrouped_data[software]
                continue
            if saida.get(software) is None:
                saida[software] = ungrouped_data[software]
            else:
                saida[software] += ungrouped_data[software]
        return saida

    def pretty_name_orgao(sigla):
        orgao_obj = Utils.create_orgao_obj()
        search = orgao_obj.search_orgao(sigla)
        pretty_name = search.results[0].pretty_name
        return pretty_name

    def orgaos_com_reports():
        orgaos = list()
        all_bases = Utils.return_all_bases_list()
        print(all_bases)
        for base in all_bases:
            if base.find('_bk') > -1:
                orgaos.append(base.split('_bk')[0])
        return orgaos

    def dict_items_indexed(data):
        index_itens = dict()
        key_number = 0
        for item in data:
            index_itens[key_number] = item
            key_number = key_number + 1
        return index_itens

    def delete_all_bases():
        orgaos_list = Utils.orgaos_com_reports()
        print(orgaos_list)
        results_list = list()
        for nm_base in orgaos_list:
            base = ReportsBase(nm_base)
            result = base.remove_base()
            results_list.append(result)
        return results_list
