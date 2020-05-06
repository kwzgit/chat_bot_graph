#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()  #问题的分类
        self.parser = QuestionPaser()  #问题的解析
        self.searcher = AnswerSearcher()  #问题的检索

    def chat_main(self, sent):
        answer = '您好，我是医药智能助理，希望可以帮到您，如果不能解决您的问题，请联系专业医生，祝您身体健康！'
        res_classify = self.classifier.classify(sent)  # 问题分类，找出相应的关系和词项
        if not res_classify:  # 词抽取不成功
            return answer
        res_sql = self.parser.parser_main(res_classify)  # 解析并生成查选cql
        final_answers = self.searcher.search_main(res_sql)  # 查选获得answer
        if not final_answers:  # 无答案，返回标准用语
            return answer
        else:
            return '\n'.join(final_answers)  # 有答案则换行返回

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小智:', answer)

