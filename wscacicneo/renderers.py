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
                temp = [key, rows[key]]
                dictlist.append(temp)

            rows = dictlist

        writer.writerow(header)
        writer.writerows(rows)

        return fout.getvalue()
