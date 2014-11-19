#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'


class Notifications(object):
    """
    Views de notificação
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request