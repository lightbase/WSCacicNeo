#!/usr/env python
# -*- coding: utf-8 -*-
from pyramid.security import (
    Allow,
    Everyone,
    )

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'user'),
                (Allow, 'Administrador', 'admin') ]
    def __init__(self, request):
        pass
