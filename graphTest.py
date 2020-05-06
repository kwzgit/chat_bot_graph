#!/usr/bin/python3
# -*- coding: utf-8 -*-
# --------------------------------
# Name graphTest
# Author DELL
# Date  2020/5/6

# -------------------------------
from py2neo import Graph
from config import GRAPH_URL, GRAPH_USER, GRAPH_PWD
g = Graph(
            GRAPH_URL,
            username=GRAPH_USER,
            password=GRAPH_PWD)
data = g.run("MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '肺炎' return m.name, r.name, n.name").data()
print(data)