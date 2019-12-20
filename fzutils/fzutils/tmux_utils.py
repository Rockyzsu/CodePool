# coding:utf-8

'''
@author = super_fazai
@File    : tmux_utils.py
@connect : superonesfazai@gmail.com
'''

"""
tmux utils
"""

from os import system as os_system
from time import sleep

from .common_utils import _print

__all__ = [
    'backstage_open_new_tmux_page',             # 后台开启tmux page
    'send_cmd_2_tmux_page_by_page_name',        # 根据page_name给窗口发送命令
    'bulk_execute_order_cmd_by_tmux_cmd_list',  # 批量执行tmux窗口命令
]

def backstage_open_new_tmux_page(page_name: str):
    """
    后台开启tmux page
    :param page_name:
    :return:
    """
    # 重复开会报
    # duplicate session: xxx[窗口名]
    os_system('tmux new -s {page_name} -d'.format(
        page_name=page_name,))

def send_cmd_2_tmux_page_by_page_name(page_name: str, target_cmd: str):
    """
    根据page_name给窗口发送命令
    :param page_name:
    :return:
    """
    os_system('tmux send -t "{page_name}" "{target_cmd}" Enter'.format(
        page_name=page_name,
        target_cmd=target_cmd,))

def bulk_execute_order_cmd_by_tmux_cmd_list(tmux_cmd_list: (list, tuple),
                                            logger=None) -> None:
    """
    批量执行tmux窗口命令
    :param tmux_cmd_list: eg: [{'page_name': 'test', 'cmd': 'cd ~ && python3', 'delay_time': 0.,}, ...]
    :return:
    """
    for item in tmux_cmd_list:
        try:
            page_name = item.get('page_name', '')
            assert page_name != ''
            target_cmd = item.get('cmd', '')
            assert target_cmd != ''
            delay_time = item.get('delay_time', 0)
        except AssertionError as e:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
            continue

        _print(
            msg='executing new_tmux_page_name: {}, cmd: {}, delay_time: {}'.format(
                page_name,
                target_cmd,
                delay_time,
            logger=logger,))
        backstage_open_new_tmux_page(page_name=page_name)
        send_cmd_2_tmux_page_by_page_name(
            page_name=page_name,
            target_cmd=target_cmd, )
        if delay_time != 0:
            _print(msg='sleep {}s ...'.format(delay_time), logger=logger)
        else:
            pass
        sleep(delay_time)