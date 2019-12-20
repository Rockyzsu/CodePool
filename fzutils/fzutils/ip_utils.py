# coding:utf-8

'''
@author = super_fazai
@File    : ip_utils.py
@connect : superonesfazai@gmail.com
'''

"""
ip utils
"""

import re
from .common_utils import json_2_dict
from .internet_utils import *
from .ip_pools import tri_ip_pool
from .spider.fz_requests import Requests

__all__ = [
    'get_ip_address_info',              # 获取ip的address信息
    'get_local_external_network_ip',    # 获取本机外网ip地址
    'proxy_type_detect',                # 代理种类发现
]

def get_ip_address_info(ip) -> dict:
    '''
    获取ip的address信息(国家), 可根据需求分装成异步的请求
    :param ip: eg: '123.13.244.44'
    :return:
    '''
    base_url = 'http://ip.taobao.com/service/getIpInfo.php'
    params = (
        ('ip', ip),
    )
    try:
        body = Requests.get_url_body(url=base_url, use_proxy=False, params=params)
        _ = json_2_dict(body).get('data', {})
        country = _.get('country', '')
        assert country != '', '获取到的country为空值!'

        return {
            'ip': ip,
            'country': country,
            'city': _.get('city', ''),
            'isp': _.get('isp', ''),
        }
    except Exception as e:
        raise e

def get_local_external_network_ip() -> str:
    '''
    获取本机外网ip地址
    :return: '' 表示获取失败!
    '''
    url = 'http://httpbin.org/get'
    local_ip = json_2_dict(Requests.get_url_body(use_proxy=False, url=url)).get('origin', '')

    return local_ip

def proxy_type_detect(ip_pool_type=tri_ip_pool):
    '''
    代理种类发现
    :return:
    '''
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_phone_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    url = 'http://proxies.site-digger.com/proxy-detect/'
    body = Requests.get_url_body(url=url, headers=headers, ip_pool_type=ip_pool_type)
    # print(body)
    try:
        REMOTE_ADDR = re.compile('REMOTE_ADDR = (.*?)</p>').findall(body)[0]
        HTTP_VIA = re.compile('HTTP_VIA = (.*?)</p>').findall(body)[0]
        HTTP_X_FORWARDED_FOR = re.compile('HTTP_X_FORWARDED_FOR = (.*?)</p>').findall(body)[0]
        HTTP_PROXY_CONNECTION = re.compile('HTTP_PROXY_CONNECTION = (.*?)</p>').findall(body)[0]
        print('REMOTE_ADDR:{}\nHTTP_VIA:{}\nHTTP_X_FORWARDED_FOR:{}\nHTTP_PROXY_CONNECTION:{}\n'.format(REMOTE_ADDR, HTTP_VIA, HTTP_X_FORWARDED_FOR, HTTP_PROXY_CONNECTION))
    except IndexError as e:
        print(e)

    return None
