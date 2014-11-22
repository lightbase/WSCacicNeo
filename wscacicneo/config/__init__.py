#!/usr/env python
# -*- coding: utf-8 -*-
#import os
#import configparser


def setup(settings):

    # config = configparser.ConfigParser()
    # here = os.path.abspath(os.path.dirname(__file__))
    # config_file = os.path.join(here, '../../development.ini')
    # config.read(config_file)

    global REST_URL
    global BULK_URL
    global TMP_DIR

    REST_URL = settings['rest_url']
    BULK_URL = settings['bulk_url']
    TMP_DIR = settings['tmp_dir']