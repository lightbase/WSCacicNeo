__author__ = 'adley'

import requests
import json
import random
from wscacicneo.utils.utils import Utils
from pyramid.httpexceptions import HTTPFound
from wscacicneo.model import config_reports
from liblightbase.lbsearch.search import NullDocument
from pyramid.session import check_csrf_token
from wscacicneo.search.orgao import SearchOrgao


class Graficos():
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    def graficos_orgao(self):
        if 'attr' in self.request.matchdict.keys():
            attr = self.request.matchdict['attr']
        else:
            attr = 'softwarelist'
        orgao = self.request.matchdict['nm_orgao']
        data = dict()
        if orgao != 'todos-orgaos':
            if attr not in ['softwarelist','todos']:
                return self.graficos(orgao = orgao)
            elif attr == 'todos':
                for attrib in ['win32_physicalmemory', 'win32_bios', 'win32_diskdrive', 'operatingsystem', 'win32_processor']:
                    data[attrib] = self.graficos(attr=attrib)['data']
                data['softwarelist'] = self.graficos_software(view_type='detailed')['data']
            else:
                return self.graficos_software(orgao)
        else:
            search = SearchOrgao()
            orgaos = [org.nome for org in search.list_by_name()]
            for org in orgaos:
                if attr != 'softwarelist':
                    data[org] = self.graficos(orgao = org)['data']
                else:
                    data[org] = self.graficos_software(org)['data']
        title_chart = ''
        # Define o nome do gráfico baseado no "attr"
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
        elif attr == "softwarelist":
            title_chart = "Gráfico de Softwares"
        elif attr != 'todos':
            title_chart = "Gráfico de "+attr

        return {"data": data,
                "usuario_autenticado": self.usuario_autenticado,
                "title_chart": title_chart,
                "orgao_nm": orgao,
                "attr": attr
        }

    def graficos(self, orgao=None, attr=None):

        # Define o nome do gráfico baseado no "attr"
        if attr is None:
            attr = self.request.matchdict['attr']
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
        else:
            title_chart = "Gráfico de "+attr

        if orgao is None:
            orgao_nm = self.request.matchdict['nm_orgao']
        else:
            orgao_nm = orgao
        nm_orgao = Utils.format_name(orgao_nm)
        reports_config = config_reports.ConfReports(nm_orgao)
        get_base = reports_config.get_attribute(attr)
        results = get_base.results
        data = []
        list_of_numbers = []
        data.append(['Item', 'Quantidade'])

        # color_list = ["#8B0000", "#191970", "#2F4F4F", "#006400", "#808000",
        #              "#696969", "#B8860B", "#FF8C00", "#2E8B57", "#228B22"]
        # chosen_color = 0

        for elm in results:
            if isinstance(elm, NullDocument):
                continue
            parent = getattr(elm, attr)
            item = getattr(parent, attr + '_item')
            amount = getattr(parent, attr + '_amount')
            data.append([item, int(amount)])
            list_of_numbers.append([int(amount)])
            # Antigo código para o Charts JS
            # data.append({"label": item, "data": int(amount), "color": color_list[chosen_color]})
            # chosen_color += 1
            # if chosen_color >= len(color_list):
            #    chosen_color = 0

        # if attr == "software":
            # max_num = Utils.getMaxOfList(list_of_numbers)

        return {"data": data,
                "usuario_autenticado": self.usuario_autenticado,
                "title_chart": title_chart,
                "orgao_nm": orgao_nm,
                "attr": attr
        }

    def graficos_software(self, orgao=None, view_type = None):

        attr = 'softwarelist'
        title_chart = "Gráfico de Softwares"
        if view_type is None:
            view_type = self.request.matchdict['view_type']
        if orgao is None:
            orgao_nm = self.request.matchdict['nm_orgao']
        else:
            orgao_nm = orgao
        nm_orgao = Utils.format_name(orgao_nm)
        reports_config = config_reports.ConfReports(nm_orgao)
        get_base = reports_config.get_attribute(attr)
        results = get_base.results
        data = []
        list_of_numbers = []
        data.append(['Item', 'Quantidade'])

        # color_list = ["#8B0000", "#191970", "#2F4F4F", "#006400", "#808000",
        #              "#696969", "#B8860B", "#FF8C00", "#2E8B57", "#228B22"]
        # chosen_color = 0

        for elm in results:
            if isinstance(elm, NullDocument):
                continue
            parent = getattr(elm, attr)
            item = getattr(parent, attr + '_item')
            amount = getattr(parent, attr + '_amount')
            data.append([item, int(amount)])
            list_of_numbers.append([int(amount)])
            # Antigo código para o Charts JS
            # data.append({"label": item, "data": int(amount), "color": color_list[chosen_color]})
            # chosen_color += 1
            # if chosen_color >= len(color_list):
            #    chosen_color = 0

        if view_type == 'simple':
            data_dict = dict()
            data.pop(0)
            for a in data:
                data_dict[a[0]]= a[1]
            data_dict = Utils.group_data(data_dict)
            data=list()
            data.append(['Item', 'Quantidade'])
            for a in data_dict.keys():
                data.append([a, int(data_dict[a])])
        #if attr == "software":
            #max_num = Utils.getMaxOfList(list_of_numbers)

        return {"data": data,
                "usuario_autenticado": self.usuario_autenticado,
                "title_chart": title_chart,
                "orgao_nm": orgao_nm,
                "attr": attr
        }