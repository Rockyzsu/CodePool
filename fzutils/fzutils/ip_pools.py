# coding:utf-8

from requests import get
import gc
import re
from gc import collect
from pickle import dumps
from random import randint
from .sql_utils import BaseRedisCli
from .safe_utils import get_uuid3
from .data.pickle_utils import deserializate_pickle_object
from .common_utils import json_2_dict
from .time_utils import *

__all__ = [
    'MyIpPools',
    'IpPools',
    'get_random_proxy_ip_from_ip_pool',
]

ip_proxy_pool = 'IPProxyPool'
fz_ip_pool = 'fz_ip_pool'
sesame_ip_pool = 'sesame_ip_pool'
tri_ip_pool = 'tri_ip_pool'

class MyIpPools(object):
    def __init__(self, type=ip_proxy_pool, high_conceal=False):
        '''
        :param type: 所使用ip池类型
        :param high_conceal: 是否初始化为高匿代理
        '''
        super(MyIpPools, self).__init__()
        self.high_conceal = high_conceal
        self.type = type
        self.redis_cli = BaseRedisCli() if self.type == fz_ip_pool or self.type == sesame_ip_pool else None
        if self.type == fz_ip_pool:
            self.h_key = get_uuid3('h_proxy_list')
        elif self.type == sesame_ip_pool:
            self.h_key = get_uuid3('sesame_ip_pool')
        else:
            self.h_key = None

    def get_proxy_ip_from_ip_pool(self):
        '''
        从代理ip池中获取到对应ip
        :return: dict类型 {'http': ['http://183.136.218.253:80', ...]}
        '''
        proxy_list = []
        if self.type == ip_proxy_pool:
            if self.high_conceal:
                base_url = 'http://127.0.0.1:8000/?types=0' # types: 0高匿|1匿名|2透明
            else:
                base_url = 'http://127.0.0.1:8000'
            try:
                result = get(base_url).json()
            except Exception as e:
                print(e)
                return {'http': None}

            for item in result:
                if item[2] > 7:
                    tmp_url = 'http://{}:{}'.format(item[0], item[1])
                    proxy_list.append(tmp_url)
                else:
                    delete_url = 'http://127.0.0.1:8000/delete?ip='
                    delete_info = get(delete_url + item[0])

        elif self.type == fz_ip_pool:
            base_url = 'http://127.0.0.1:8002/get_all'
            # mac 内网读取树莓派的服务(本地不开, ip池白名单冲突!)
            # base_url = 'http://192.168.2.112:8001/get_all'
            try:
                res = get(base_url).json()
                assert res != [], 'res为空list!'
            except Exception as e:
                print(e)
                return {'https': None}

            proxy_list = ['http://{}:{}'.format(item['ip'], item['port']) for item in res]

        elif self.type == sesame_ip_pool:
            _ = json_2_dict(self.redis_cli.get(name=self.h_key) or dumps([]), default_res=[])
            proxy_list = []
            for i in _:
                if datetime_to_timestamp(string_to_datetime(i.get('expire_time', ''))) \
                        > datetime_to_timestamp(get_shanghai_time()) + 15:
                    proxy_list.append('http://{}:{}'.format(i.get('ip', ''), i.get('port', '')))

        elif self.type == tri_ip_pool:
            base_url = 'http://127.0.0.1:8001/get_all'
            try:
                res = get(base_url).json()
                assert res != [], 'res为空list!'
            except Exception as e:
                print(e)
                return {'https': None}

            proxy_list = ['http://{}:{}'.format(item['ip'], item['port']) for item in res]

            return {
                'https': proxy_list,
            }

        else:
            raise ValueError('type值异常, 请检查!')

        return {
            'http': proxy_list,
        }

    def _get_random_proxy_ip(self):
        '''
        随机获取一个代理ip: 格式 'http://175.6.2.174:8088'
        :return:
        '''
        _ = self.get_proxy_ip_from_ip_pool()
        ip_list = _.get('http') if _.get('http') is not None else _.get('https')
        try:
            if isinstance(ip_list, list):
                proxy_ip = ip_list[randint(0, len(ip_list) - 1)]  # 随机一个代理ip
            else:
                raise TypeError
        except Exception:
            print('从ip池获取随机ip失败...正在使用本机ip进行爬取!')
            proxy_ip = False

        return proxy_ip

    def _empty_ip_pools(self):
        '''
        清空ip池
        :return:
        '''
        if self.type == ip_proxy_pool:
            base_url = 'http://127.0.0.1:8000'
            result = get(base_url).json()
            delete_url = 'http://127.0.0.1:8000/delete?ip='

            for item in result:
                if item[2] < 11:
                    delete_info = get(delete_url + item[0])
                    print(delete_info.text)
        elif self.type == fz_ip_pool or self.type == sesame_ip_pool:
            self.redis_cli.set(self.h_key, '')

        return None

    def __del__(self):
        try:
            del self.redis_cli
        except:
            pass
        collect()

class IpPools(MyIpPools):
    pass

def get_random_proxy_ip_from_ip_pool(ip_pool_type=tri_ip_pool, high_conceal=True) -> str:
    '''
    得到一个随机代理
    :return: str 格式: ip:port or ''
    '''
    ip_object = IpPools(type=ip_pool_type, high_conceal=high_conceal)
    _ = ip_object._get_random_proxy_ip()
    proxy_ip = re.compile(r'https://|http://').sub('', _) if isinstance(_, str) else ''
    # print(proxy_ip)

    return proxy_ip

