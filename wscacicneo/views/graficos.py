__author__ = 'adley'

import requests
import json
import random
from wscacicneo.utils.utils import Utils
from pyramid.httpexceptions import HTTPFound
from wscacicneo.model import config_reports
from liblightbase.lbsearch.search import NullDocument
from pyramid.session import check_csrf_token


class Graficos():
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    def graficos(self):
        attr = self.request.matchdict['attr']
        orgao_nm = self.request.matchdict['nm_orgao']
        nm_orgao = Utils.format_name(orgao_nm)
        reports_config = config_reports.ConfReports(nm_orgao)
        get_base = reports_config.get_attribute(attr)
        results = get_base.results
        data = []
        list_of_numbers = []
        data.append(['Item', 'Quantidade'])

        #color_list = ["#8B0000", "#191970", "#2F4F4F", "#006400", "#808000",
        #              "#696969", "#B8860B", "#FF8C00", "#2E8B57", "#228B22"]
        #chosen_color = 0

        #Define o nome do gráfico baseado no "attr"
        if attr == "win32_processor":
            title_chart = "Gráfico de Processadores"
        elif attr == "win32_diskdrive":
            title_chart = "Gráfico de HD"
        elif attr == "win32_bios":
            title_chart = "Gráfico de BIOS"
        elif attr == "win32_physicalmemory":
            title_chart = "Gráfico de Memória"
        elif attr == "operatingsystem":
            title_chart = "Gráfico de Sistemas Operacionais"
        elif attr == "software":
            title_chart = "Gráfico de Softwares"
        else:
            title_chart = "Gráfico de "+attr

        for elm in results:
            if isinstance(elm, NullDocument):
                continue
            parent = getattr(elm, attr)
            item = getattr(parent, attr + '_item')
            amount = getattr(parent, attr + '_amount')
            data.append([item, int(amount)])
            list_of_numbers.append([int(amount)])
            print(data)
            # Antigo código para o Charts JS
            #data.append({"label": item, "data": int(amount), "color": color_list[chosen_color]})
            #chosen_color += 1
            #if chosen_color >= len(color_list):
            #    chosen_color = 0

        if attr == "software":
            #max_num = Utils.getMaxOfList(list_of_numbers)
            print(list_of_numbers)

        return {"data": data,
                "usuario_autenticado": self.usuario_autenticado,
                "title_chart": title_chart,
        }