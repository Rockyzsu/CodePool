# coding:utf-8

'''
@author = super_fazai
@File    : twisted_utils.py
@connect : superonesfazai@gmail.com
'''

"""
twisted utils
"""

from pprint import pprint
from twisted.internet import defer as twisted_defer
from twisted.internet import reactor as twisted_reactor
from twisted.internet import threads as twisted_threads
from twisted.python import threadable as twisted_threadable
from twisted.internet.interfaces import IReactorTime

from .common_utils import _print

__all__ = [
    'handle_deferred_list_res',         # 处理延时列表的结果集得到结果集合(获取one_res)
]

def handle_deferred_list_res(deferred_list_res: list) -> list:
    """
    处理延时列表的结果集得到结果集合(获取one_res)
    :param deferred_list_res: 延迟列表结果集合
    :return:
    """
    one_res = []
    for i in deferred_list_res:
        # _print(msg=str(i))
        for j in i:
            # _print(msg='item: {}'.format(j))
            one_res.append(j[1])

    return one_res