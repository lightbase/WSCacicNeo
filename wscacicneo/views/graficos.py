__author__ = 'adley'

import requests
import json
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

    def graficos(self):
        attr = self.request.matchdict['attr']
        orgao_nm = self.request.matchdict['nm_orgao']
        usuario_autenticado = Utils.retorna_usuario_autenticado(email=self.request.authenticated_userid)
        nm_orgao = Utils.format_name(orgao_nm)
        reports_config = config_reports.ConfReports(nm_orgao)
        get_base = reports_config.get_attribute(attr)
        results = get_base.results
        data = []
        for elm in results:
            if isinstance(elm, NullDocument):
                continue
            parent = getattr(elm, attr)
            item = getattr(parent, attr+'_item')
            amount = getattr(parent, attr+'_amount')
            data.append({"item_name": item, "quantidade": amount})
        return {"data": data,
                 "usuario_autenticado": usuario_autenticado
                 }