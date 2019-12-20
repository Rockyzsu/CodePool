# coding:utf-8

'''
@author = super_fazai
@File    : my_requests.py
@Time    : 2017/3/22 10:13
@connect : superonesfazai@gmail.com
'''

import better_exceptions
better_exceptions.hook()

import sys
sys.path.append('..')

import requests
import re
import gc
from random import randint
from pprint import pprint

# 避免报安全异常!
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from ..ip_pools import (
    MyIpPools,
    ip_proxy_pool,
    fz_ip_pool,
    sesame_ip_pool,
    tri_ip_pool,)
from ..internet_utils import get_base_headers
from ..common_utils import _print

__all__ = [
    'MyRequests',
    'Requests',
]

# 代理类型
PROXY_TYPE_HTTP = 'http'
PROXY_TYPE_HTTPS = 'https'

class MyRequests(object):
    def __init__(self):
        super(MyRequests, self).__init__()

    @classmethod
    def get_url_body(cls,
                     url,
                     use_proxy=True,
                     headers:dict=get_base_headers(),
                     params=None,
                     data=None,
                     cookies=None,
                     had_referer=False,
                     encoding='utf-8',
                     method='get',
                     timeout=12,
                     num_retries=1,
                     high_conceal=True,
                     ip_pool_type=ip_proxy_pool,
                     verify=None,
                     _session=None,
                     get_session=False,
                     proxies=None,
                     proxy_type=PROXY_TYPE_HTTP,):
        '''
        根据url得到body
        :param url:
        :param use_proxy: 是否使用代理模式, 默认使用
        :param headers:
        :param params:
        :param data:
        :param cookies:
        :param had_referer:
        :param encoding:
        :param method:
        :param timeout:
        :param num_retries:
        :param high_conceal: 代理是否为高匿名
        :param verify:
        :param _session: 旧的session
        :param get_session: True 则返回值为此次请求的session
        :param proxies: 代理 None or {xxx} 同requests的proxies
        :param proxy_type: PROXY_TYPE_HTTP 即'http' or PROXY_TYPE_HTTPS 即'https'
        :return: '' 表示error | str 表示success
        '''
        def _get_one_proxies_obj():
            '''获取一个代理'''
            tmp_proxies = {}
            if proxies is None:
                if use_proxy:
                    # 设置代理ip
                    tmp_proxies = cls._get_proxies(
                        ip_pool_type=ip_pool_type,
                        high_conceal=high_conceal,
                        proxy_type=proxy_type)
                    assert tmp_proxies != {}, '获取代理失败, 此处跳过!'
                    # print('------>>>| 正在使用代理ip: {} 进行爬取... |<<<------'.format(tmp_proxies.get('http')))
                else:
                    pass
            else:
                if isinstance(proxies, dict):
                    tmp_proxies = proxies
                else:
                    raise ValueError('proxies类型异常!')

            return tmp_proxies

        # print('num_retries = {}'.format(num_retries))

        try:
            tmp_proxies = _get_one_proxies_obj()
        except Exception as e:
            print(e)
            return ''

        tmp_headers = headers
        tmp_headers['Host'] = re.compile(r'://(.*?)/').findall(url)[0]
        if had_referer:
            if re.compile(r'https').findall(url) != []:
                tmp_headers['Referer'] = 'https://' + tmp_headers['Host'] + '/'
            else:
                tmp_headers['Referer'] = 'http://' + tmp_headers['Host'] + '/'

        with requests.session() if _session is None else _session as s:
            try:
                response = s.request(
                    method=method,
                    url=url,
                    headers=tmp_headers,
                    params=params,
                    data=data,
                    cookies=cookies,
                    proxies=tmp_proxies,
                    timeout=timeout,
                    verify=verify)  # 在requests里面传数据，在构造头时，注意在url外头的&xxx=也得先构造
                # print(str(response.url))
                try:
                    _ = response.content.decode(encoding)
                except Exception:  # 报编码错误
                    _ = response.text
                body = cls._wash_html(_)
                # print(str(body))

            except Exception as e:
                # print(e)
                if num_retries > 1:
                    return cls.get_url_body(
                        url=url,
                        use_proxy=use_proxy,
                        headers=tmp_headers,
                        params=params,
                        data=data,
                        cookies=cookies,
                        had_referer=had_referer,
                        encoding=encoding,
                        method=method,
                        timeout=timeout,
                        num_retries=num_retries-1,
                        high_conceal=high_conceal,
                        ip_pool_type=ip_pool_type,
                        verify=verify,
                        _session=_session,
                        get_session=get_session,
                        proxies=proxies,
                        proxy_type=proxy_type,)
                else:
                    print('requests.get()请求超时....')
                    print('data为空!')
                    body = ''

        if get_session:
            return s

        return body

    @classmethod
    def _wash_html(cls, body):
        body = re.compile('\t|  ').sub('', body)
        body = re.compile('\r\n').sub('', body)
        body = re.compile('\n').sub('', body)

        body = re.compile('<ahref').sub('<a href', body)
        body = re.compile('<strongtitle').sub('<strong title', body)

        return body

    @classmethod
    def _get_proxies(cls, ip_pool_type=ip_proxy_pool, high_conceal=True, proxy_type=PROXY_TYPE_HTTP):
        '''
        得到单个代理ip
        :return: 格式: {'http': ip+port} | 异常返回 {}
        '''
        ip_obj = MyIpPools(type=ip_pool_type, high_conceal=high_conceal)
        proxies = ip_obj.get_proxy_ip_from_ip_pool()  # {'http': ['xx', 'yy', ...]}
        _ = proxies.get('http') if proxies.get('http') is not None else proxies.get('https')
        try:
            proxy = _[randint(0, len(_) - 1)]
        except TypeError:
            return {}

        if ip_pool_type == sesame_ip_pool:
            return {
                'https': proxy,
            }

        if ip_pool_type == tri_ip_pool:
            # return {
            #     'http': proxy,
            # }
            pass

        if proxy_type == PROXY_TYPE_HTTP:
            return {
                'http': proxy
            }

        elif proxy_type == PROXY_TYPE_HTTPS:
            return {
                'https': proxy,
            }

        else:
            raise ValueError('未知的proxy_type值!请检查!')

    @classmethod
    def _download_file(cls,
                       url,
                       file_save_path,
                       headers=None,
                       params=None,
                       cookies=None,
                       use_proxy=True,
                       ip_pool_type=ip_proxy_pool,
                       high_conceal=True) -> bool:
        '''
        下载文件
        :param url:
        :param file_save_path: 文件存储路径
        :param use_proxy: 是否使用代理
        :return:
        '''
        if use_proxy:
            tmp_proxies = cls._get_proxies(ip_pool_type=ip_pool_type, high_conceal=high_conceal)
            if tmp_proxies == {}:
                print('获取代理失败, 此处跳过!')
                return False
        else:
            tmp_proxies = {}

        with requests.get(url=url, headers=headers, params=params, cookies=cookies, proxies=tmp_proxies, stream=True) as response:
            chunk_size = 1024                                       # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            if response.status_code == 200:
                with open(file_save_path, 'wb') as f:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
            else:
                return False

        return True

    def __del__(self):
        gc.collect()

class Requests(MyRequests):
    '''改名'''
    pass
