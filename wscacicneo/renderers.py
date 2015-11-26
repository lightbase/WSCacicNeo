#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import csv

try:
    from StringIO import StringIO # python 2
except ImportError:
    from io import StringIO # python 3


class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        """ Returns a plain CSV-encoded string with content-type
        ``text/csv``. The content-type may be overridden by
        setting ``request.response.content_type``."""

        request = system.get('request')
        if request is not None:
            response = request.response
            ct = response.content_type
            if ct == response.default_content_type:
                response.content_type = 'text/csv'
                #response.charset = 'utf8'

        fout = StringIO()
        writer = csv.writer(fout, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        header = value.get('header', [])
        rows = value.get('rows', [])

        if isinstance(rows, dict):
            # Converte dict para list
            dictlist = list()
            for key in rows.keys():
                if isinstance(rows[key], dict):
                    for attr in rows[key].keys():
                        if isinstance(rows[key][attr], dict):
                            for item in rows[key][attr].keys():
                                temp = [item, rows[key][attr][item], self.item_pretty_name(attr), key]
                                dictlist.append(temp)
                        else:
                            temp = [attr, rows[key][attr], self.item_pretty_name(key)]
                            dictlist.append(temp)
                else:
                    temp = [key, rows[key]]
                    dictlist.append(temp)

            rows = dictlist

        writer.writerow(header)
        writer.writerows(rows)

        return fout.getvalue()

    def item_pretty_name(self, item):
        if item in ['softwarelist','win32_physicalmemory',
                     'win32_bios', 'win32_diskdrive',
                     'operatingsystem', 'win32_processor']:
            if item == 'softwarelist':
                return 'Software'
            elif item == 'win32_physicalmemory':
                return 'Memória'
            elif item == 'win32_bios':
                return 'BIOS'
            elif item == 'win32_diskdrive':
                return 'HD'
            elif item == 'win32_processor':
                return 'Processador'
            elif item == 'operatingsystem':
                return 'Sistema Operacional'
        else:
            return item