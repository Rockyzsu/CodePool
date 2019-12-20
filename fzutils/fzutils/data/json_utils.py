# coding:utf-8

'''
@author = super_fazai
@File    : json_utils.py
@Time    : 2016/7/25 09:43
@connect : superonesfazai@gmail.com
'''

import re
from decimal import Decimal
from datetime import datetime

from ..common_utils import json_2_dict

__all__ = [
    'read_json_from_local_json_file',                       # 从本地json文件读取json, 并以dict返回
    'nonstandard_json_str_handle',                          # 不规范的json_str处理
    'get_new_list_by_handle_list_2_json_error',             # 处理list转json时, json无法处理某些类型
    'get_some_type_json_can_recognize',                     # 处理得到json能识别的类型
]

def read_json_from_local_json_file(json_file_path):
    '''
    从本地json文件读取json, 并以dict返回
    :param json_file_path:
    :return: a dict
    '''
    try:
        result = ''
        with open(json_file_path, 'r') as file:
            for item in file.readlines():
                result += item.replace('\n', '')
    except FileNotFoundError as e:
        print('json path 文件不存在, 请检查!')
        raise e

    # print(result)
    _ = json_2_dict(json_str=result)

    return _

def nonstandard_json_str_handle(json_str):
    '''
    不规范的json_str处理
    :param json_str:
    :return:
    '''
    json_str = re.compile('null').sub('""', json_str)
    json_str = re.compile(':,').sub(':"",', json_str)

    return json_str

def get_new_list_by_handle_list_2_json_error(target_list: (tuple, list)) -> list:
    """
    处理list转json时, json无法处理某些类型(测试重写json.JSONEncoder, 实际无法成功处理异常, 故单独转换)
    :param target_list:
    :return:
    """
    new_item = []
    for i in target_list:
        i = get_some_type_json_can_recognize(target=i)
        new_item.append(i)

    return new_item

def get_some_type_json_can_recognize(target):
    """
    处理得到json能识别的类型
    :param target: dict or list中无法被识别的python类型
    :return:
    """
    if isinstance(target, Decimal):
        # 处理json无法转decimal
        target = float(target)
    elif isinstance(target, datetime):
        # 处理json无法转datetime
        target = target.strftime('%Y-%m-%d %H:%M:%S')
    else:
        pass

    return target



