#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import os
from .. import config
from paste.deploy.loadwsgi import appconfig

# Configurações de teste
here = os.path.abspath(os.path.dirname(__file__))
config_dir = os.path.join(here, '../../')
settings = appconfig('config:test.ini', relative_to=config_dir)
config.setup(settings)