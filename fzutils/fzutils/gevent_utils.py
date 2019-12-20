# coding:utf-8

'''
@author = super_fazai
@File    : gevent_utils.py
@connect : superonesfazai@gmail.com
'''

"""
gevent utils
"""

from pprint import pprint
from gevent import sleep as gevent_sleep
from gevent import joinall as gevent_joinall
from gevent import Timeout as GeventTimeout
from gevent.pool import Pool as GeventPool
from gevent import monkey as gevent_monkey
from gevent import (
    Greenlet,
)

from .common_utils import _print

# 猴子补丁
# TODO 全部替换
# gevent_monkey.patch_all()
# TODO sql 连接只需针对socket连接的替换即可
# gevent_monkey.patch_socket()

def wait_for_every_greenlet_obj_run_over_and_get_tasks_res(tasks: list,
                                                           gevent_joinall_timeout=None,
                                                           gevent_joinall_raise_error: bool=True,
                                                           gevent_joinall_count=None,
                                                           logger=None) -> list:
    """
    等待tasks中所有greenlet_obj执行结束并获取执行结果
    simple use:
        def do_something(index):
            return 'xxx'

        tasks = []
        for index in range(1, 100):
            print('create task[where is index: {}] ...'.format(index))
            tasks.append(gevent_spawn(
                do_something,
                index,
            ))
        one_res = wait_for_every_greenlet_obj_run_over_and_get_tasks_res(tasks=tasks)

    :param tasks: [<Greenlet at 0x11719a348: _run>, ...]
    :param gevent_joinall_timeout:
    :param gevent_joinall_raise_error:
    :param gevent_joinall_count:
    :param logger:
    :return:
    """
    from time import time

    s_time = time()
    one_res = []
    try:
        _print(msg='请耐心等待所有任务完成...', logger=logger)
        # list 里面item是<Greenlet at 0x11719a348: _run>
        tmp = gevent_joinall(
            greenlets=tasks,
            timeout=gevent_joinall_timeout,
            raise_error=gevent_joinall_raise_error,
            count=gevent_joinall_count,)

        # 获取所有执行结果
        for item in tmp:
            res = item.get()
            one_res.append(res)
        # pprint(one_res)
        _print(
            msg='此次耗时 {} s!'.format(round(float(time() - s_time), 3)),
            logger=logger)

    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        return one_res

    return one_res