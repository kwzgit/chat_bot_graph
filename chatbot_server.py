#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""分诊服务器
"""

import json
import sys
import traceback
from flask import Flask, request, Response

sys.path.append('..')
from config import IP, PORT
from chatbot_graph import ChatBotGraph

app = Flask(__name__)
chat_bot = ChatBotGraph()


@app.after_request
def cors(environ):  # 防止跨域问题
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


def get_request_json():
    """
    :return: dict, {medical_text_type_1:content_1, ...}
    """
    json_request = {}
    try:
        if request.get_data():
            params = json.loads(request.get_data())  # 获取json
            json_request = params
    except:
        traceback.print_exc()
        print('-- 请求参数获取错误')

    return json_request


@app.route('/api/chat_bot', methods=['POST', 'GET'])
def predict():
    """预测
    """
    response_json = {'status':False}
    try:
        request_param = get_request_json()
        question = request_param['question']
        answer = chat_bot.chat_main(question)
        response_json['answer'] = answer
        response_json['status'] = True

    except:
        traceback.print_exc()

    finally:
        return Response(json.dumps(response_json, ensure_ascii=False), mimetype='application/json')


if __name__ == '__main__':
    # 获取本机电脑名和ip
    ip = IP
    port = PORT
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    app.run(host=ip, port=port)
