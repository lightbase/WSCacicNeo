#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

from beaker.cache import cache_region


@cache_region('long_term')
def processor_converter(value):
    """
    Converte a string no processor family do WMI
    :param value: valor inteiro a procurar
    :return: str com a descição
    """
    # FIXME: não encontrei uma forma de identificar o processor family no OCS

    return 2


@cache_region('long_term')
def memory_converter(value):
    """
    Converte o valor recebido para um memorytype cadastrado
    :param value: valor inteiro lido no Agente
    :return: str com o valor da descrição
    """
    # FIXME: colocar todos os modelos aqui 
    memory_types = {
        '0': 'Unknown',
        '1': 'Other',
        '2': 'DRAM',
        '9': 'RAM',
        '10': 'ROM',
        '11': 'Flash',
        '12': 'DDR',
        '21': 'DDR-2'
    }
    saida = memory_types.get(value)
    if saida is None:
        # Retorna 0 como padrão
        saida = 0

    return saida
