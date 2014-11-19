#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import os
from .. import config
from paste.deploy.loadwsgi import appconfig
from pyramid import testing


def setup_package():
    """
    Setup test data for the package
    """
    # Configurações de teste
    here = os.path.abspath(os.path.dirname(__file__))
    config_dir = os.path.join(here, '../../')
    settings = appconfig('config:test.ini', relative_to=config_dir)
    config.setup(settings)
    conf = testing.setUp(settings=settings)


def teardown_package():
    """
    Remove test data
    """
    pass