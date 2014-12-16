__author__ = 'adley'

import requests
import json
import random
from wscacicneo.utils.utils import Utils
from pyramid.httpexceptions import HTTPFound
from wscacicneo.model import config_reports
from liblightbase.lbsearch.search import NullDocument


class Graficos():
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            user_id=self.request.session.get('userid'))

    def graficos(self):
        attr = self.request.matchdict['attr']
        orgao_nm = self.request.matchdict['nm_orgao']
        nm_orgao = Utils.format_name(orgao_nm)
        reports_config = config_reports.ConfReports(nm_orgao)
        get_base = reports_config.get_attribute(attr)
        results = get_base.results
        data = []
        color_list = ["#8B0000", "#191970", "#2F4F4F", "#006400", "#808000",
                      "#696969", "#B8860B", "#FF8C00", "#2E8B57", "#228B22"]
        chosen_color = 0
        for elm in results:
            if isinstance(elm, NullDocument):
                continue
            parent = getattr(elm, attr)
            item = getattr(parent, attr + '_item')
            amount = getattr(parent, attr + '_amount')
            data.append({"label": item, "data": int(amount), "color": color_list[chosen_color]})
            chosen_color += 1
            if chosen_color >= len(color_list):
                chosen_color = 0
        return {"data": data,
                "usuario_autenticado": self.usuario_autenticado,
        }