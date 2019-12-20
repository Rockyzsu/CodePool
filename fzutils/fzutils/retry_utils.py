# coding:utf-8

'''
@author = super_fazai
@File    : retry_utils.py
@connect : superonesfazai@gmail.com
'''

from tenacity import retry as tenacity_retry
from tenacity import (
    stop_after_delay,
    stop_after_attempt,)