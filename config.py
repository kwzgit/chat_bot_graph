#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
DICT_PATH = os.path.join(PROJECT_PATH, 'dict')
DATA_PATH = os.path.join(PROJECT_PATH, 'data')

IP = '192.168.3.180'
PORT = '9999'

GRAPH_URL = 'http://192.168.3.150:7474'
GRAPH_USER = 'neo4j'
GRAPH_PWD = '12345678'