# coding:utf-8

'''
@author = super_fazai
@File    : map_utils.py
@connect : superonesfazai@gmail.com
'''

"""
map utils
"""

from .internet_utils import get_base_headers
from .common_utils import json_2_dict
from .aio_utils import unblock_request

__all__ = [
    'async_get_location_info_by_lng_and_lat',     # 异步通过经纬度在百度地图api中获取定位信息(得设置白名单)
]

async def async_get_location_info_by_lng_and_lat(baidu_api_key:str, lng:float, lat:float) -> dict:
    '''
    异步通过经纬度在百度地图api中获取定位信息(得设置ip白名单)
    :param baidu_api_key:
    :param lng:
    :param lat:
    :return:
    '''
    url = 'http://api.map.baidu.com/geocoder'
    params = (
        ('location', ('{},{}'.format(lat, lng))),
        ('output', 'json'),
        ('key', baidu_api_key),
    )
    return json_2_dict(
        json_str=await unblock_request(url=url, headers=get_base_headers(), params=params),
        default_res={})
