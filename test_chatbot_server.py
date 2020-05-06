#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""bio服务测试文件
"""
import os
import sys
import requests, json

sys.path.append('..')

from config import IP, PORT

doc = '''起病急骤，全身症状有高热、寒战、厌食、乏力等，局部症状有尿频、尿急、尿痛及直肠刺激症状'''


def test_with_file():
    """用文件去测试
    """
    url = 'http://{}:{}/api/chat_bot'.format(IP, PORT)
    json_obj = {
        'question': '肺炎的症状',  # 现病史

    }
    data = json.dumps(json_obj)
    res = requests.post(url, data)  # 发送请求
    print(res.content.decode('utf-8'))


def main():
    """"""
    # for i in range(100):
    test_with_file()
    # test_similarity()

if __name__ == '__main__':
    main()