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
    global DB_NAME
    global DB_USER
    global DB_PASS
    global DB_HOST
    global SCHEMA_NAME
    global LBRELACIONAL_URL
    #global TMP_DIR

    REST_URL = settings['rest_url']
    BULK_URL = settings['bulk_url']
    #TMP_DIR = settings['tmp_dir']
    DB_NAME = settings['dbName']
    DB_USER = settings['dbUser']
    DB_PASS = settings['dbPass']
    DB_HOST = settings['dbHost']
    SCHEMA_NAME = settings['schema_name']
    LBRELACIONAL_URL = settings['lbrelacional_url']
