#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node
from config import GRAPH_URL, GRAPH_USER, GRAPH_PWD, DATA_PATH


class MedicalGraph:
    def __init__(self):
        self.data_path = os.path.join(DATA_PATH, 'medical.json')
        self.g = Graph(
            host=GRAPH_URL,  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            username=GRAPH_USER,  # 数据库user name，如果没有更改过，应该是neo4j
            password=GRAPH_PWD)

    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        drugs = [] # 药品
        foods = [] #　食物
        checks = [] # 检查
        departments = [] #科室
        producers = [] #药品大类
        diseases = [] #疾病
        symptoms = []#症状
        disease_infos = []#疾病信息

        # 构建节点实体关系---11
        rels_department = [] #　科室－科室关系
        rels_noteat = [] # 疾病－忌吃食物关系
        rels_doeat = [] # 疾病－宜吃食物关系
        rels_recommandeat = [] # 疾病－推荐吃食物关系
        rels_commonddrug = [] # 疾病－通用药品关系
        rels_recommanddrug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_drug_producer = [] # 厂商－药物关系
        rels_symptom = [] #疾病症状关系
        rels_acompany = [] # 疾病并发关系
        rels_category = [] #　疾病与科室之间的关系

        count = 0
        for data in open(self.data_path,encoding="utf-8"):
            #print(data)
            disease_dict = {}
            count += 1
            #print(count)
            data_json = json.loads(data)
            #print(data_json)
            disease = data_json['name']
            #print(disease)  #肺心病
            diseases.append(disease)

            disease_dict['name'] = disease
            #print(disease_dict)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:  #疾病和症状之间的关系链接
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:  #疾病和并发症的关联
                    rels_acompany.append([disease, acompany])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']
                #print(disease_dict['easy_get'] ) #女性失眠更常见。离婚、丧偶或分居是失眠的危险因素，失眠亦与社会经济地位较低有关

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                #print(cure_department)
                if len(cure_department) == 1:
                     rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])  #科室之间的关系
                    rels_category.append([disease, small])  #疾病和科室之间的关系
                disease_dict['cure_department'] = cure_department
                departments += cure_department
                #print(departments)
            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']
                #print(disease_dict['cure_way'])

            if  'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease, drug]) #疾病和药物之间的关系
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug]) #疾病和推荐药物之间的关系

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])  #疾病和不能吃的食物之间的关系
                #print(len(rels_noteat))

                foods += not_eat
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do]) #疾病和能吃的食物之间的关系

                foods += do_eat
                recommand_eat = data_json['recommand_eat']

                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand]) #疾病和推荐吃的食物之间的关系
                #print(len(rels_recommandeat))
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check]) #疾病和检查之间的关系
                checks += check
            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                #print(drug_detail)
                producer = [i.split('(')[0] for i in drug_detail]
                #print(producer)
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail] #药物和厂商之间的关系
                #print(rels_drug_producer)
                producers += producer
            #print(disease_dict,"\n")
            disease_infos.append(disease_dict)
        #print(rels_symptom) #['肛门外伤', '肛门反射减弱或消失']
        #print(len(disease_infos))
        #print(diseases)

        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases),\
               disease_infos,\
               rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, \
               rels_drug_producer, rels_recommanddrug,\
               rels_symptom, rels_acompany, rels_category

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, disease_infos):   #8808种疾病，也就是创建8808种中西疾病的节点
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
            self.g.create(node)  #
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''   #中心疾病的节点加上六个节点，一共7个节点
    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, \
        Diseases, disease_infos,rels_check, rels_recommandeat, rels_noteat,\
        rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, \
        rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_diseases_nodes(disease_infos)  #1个中心，6个连接点
        self.create_node('Drug', Drugs)
        print(len(Drugs))
        self.create_node('Food', Foods)
        print(len(Foods))
        self.create_node('Check', Checks)
        print(len(Checks))
        self.create_node('Department', Departments)
        print(len(Departments))
        self.create_node('Producer', Producers)
        print(len(Producers))
        self.create_node('Symptom', Symptoms)
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat,\
        rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom,\
        rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱') #40267
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')  #22278
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        #print("+++++",start_node,end_node)
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))

        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            #print("------p",p)
            #print("++++q",q)
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, \
        disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department,\
        rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, \
        rels_category = self.read_nodes()
        #print(Diseases)
        f_drug = open(os.path.join(DATA_PATH, 'drug.txt'), 'w')
        f_food = open(os.path.join(DATA_PATH, 'food.txt'), 'w')
        f_check = open(os.path.join(DATA_PATH, 'check.txt'), 'w')
        f_department = open(os.path.join(DATA_PATH, 'department.txt'), 'w')
        f_producer = open(os.path.join(DATA_PATH, 'producer.txt'), 'w')
        f_symptom = open(os.path.join(DATA_PATH, 'symptoms.txt'), 'w')
        f_disease = open(os.path.join(DATA_PATH, 'disease.txt'), 'w')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()
        #print("-----")
        return


if __name__ == '__main__':
    handler = MedicalGraph()
    handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()
