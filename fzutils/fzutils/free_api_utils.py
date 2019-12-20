# coding:utf-8

'''
@author = super_fazai
@File    : free_api_utils.py
@connect : superonesfazai@gmail.com
'''

"""
一些免费api 接口的封装
"""

from pprint import pprint
import re

# from fzutils.ip_pools import tri_ip_pool
# from fzutils.spider.fz_requests import Requests
# from fzutils.common_utils import json_2_dict
# from fzutils.internet_utils import (
#     get_base_headers,)

from .ip_pools import tri_ip_pool
from .spider.fz_requests import Requests
from .common_utils import json_2_dict
from .internet_utils import (
    get_base_headers,)

__all__ = [
    'get_jd_one_goods_price_info',                              # 获取京东单个商品价格
    'get_express_info',                                         # 获取快递信息
    'get_phone_num_info',                                       # 获取手机号信息
    'get_baidu_baike_info',                                     # 获取某关键字的百度百科信息

    # map
    'get_bd_map_shop_info_list_by_keyword_and_area_name',       # 根据关键字和区域检索店铺信息(百度api 关键字搜索服务)[测试最多前400个]
    'get_gd_map_shop_info_list_by_keyword_and_area_name',       # 根据关键字和区域检索店铺信息(高德api 关键字搜索服务)
    'get_gd_input_prompt_info',                                 # 根据关键字和城市名获取输入提示(高德api)
    'get_gd_reverse_geocode_info',                              # 根据地址str获取逆向地理编码(高德api)
    'get_gd_map_shop_info_list_by_lng_and_lat_and_keyword',     # 根据经纬度(主要根据), 关键字(附加条件)等条件检索附近店铺信息(高德api 关键字搜索服务)
    'get_gd_map_shop_info_list_by_gd_id',                       # 根据gd_id来得到指定的shop info list(一般为第一个)[测试发现不准确, 根据id, 常返回不相干商家]
]

def get_jd_one_goods_price_info(goods_id) -> list:
    '''
    获取京东单个商品价格
    :param goods_id: 商品id
    :return:
    '''
    base_url = 'http://p.3.cn/prices/mgets'
    params = (
        ('skuIds', 'J_' + goods_id),
    )
    body = Requests.get_url_body(url=base_url, use_proxy=False, params=params)

    return json_2_dict(body, default_res=[])

def get_express_info(express_type, express_id) -> dict:
    '''
    获取快递信息
    express_type: ps: 传字典对应的value
        {
            '申通': 'shentong',
            'ems': 'ems',
            '顺丰': 'shunfeng',
            '圆通': 'yuantong',
            '中通': 'zhongtong',
            '韵达': 'yunda',
            '天天': 'tiantian',
            '汇通': 'huitongkuaidi',
            '全峰': 'quanfengkuaidi',
            '德邦': 'debangwuliu',
            '宅急送': 'zhaijisong',
            ...
        }
    :param express_type: 快递公司名
    :param express_id: 快递号
    :return:
    '''
    base_url = 'http://www.kuaidi100.com/query'
    params = (
        ('type', express_type),
        ('postid', express_id),
    )
    body = Requests.get_url_body(url=base_url, use_proxy=False, params=params)

    return json_2_dict(body)

def get_phone_num_info(phone_num) -> dict:
    '''
    获取手机号信息
    :param phone_num: 手机号
    :return:
    '''
    url = 'https://tcc.taobao.com/cc/json/mobile_tel_segment.htm'
    params = (
        ('tel', str(phone_num)),
    )

    body = Requests.get_url_body(url=url, params=params, use_proxy=False)
    try:
        res = re.compile('__GetZoneResult_ = (.*)').findall(body)[0]
        return json_2_dict(res)
    except IndexError:
        return {}

def get_baidu_baike_info(keyword, bk_length=1000) -> dict:
    '''
    获取某关键字的百度百科信息
    :param keyword:
    :return:
    '''
    url = 'http://baike.baidu.com/api/openapi/BaikeLemmaCardApi'
    params = (
        ('scope', '103'),
        ('format', 'json'),
        ('appid', '379020'),
        ('bk_key', str(keyword)),
        ('bk_length', str(bk_length)),
    )
    body = Requests.get_url_body(
        url=url,
        params=params,
        use_proxy=False)

    return json_2_dict(body)

def get_bd_map_shop_info_list_by_keyword_and_area_name(ak:str,
                                                       keyword:str,
                                                       area_name:str,
                                                       page_num:int,
                                                       page_size:int=20,
                                                       use_proxy=True,
                                                       ip_pool_type=tri_ip_pool,
                                                       num_retries=6,
                                                       timeout=20,
                                                       logger=None,) -> list:
    """
    根据关键字和区域检索店铺信息(百度api 关键字搜索服务)[测试最多前400个]
    :param ak: 百度地图申请的ak
    :param keyword: eg: '鞋子'
    :param area_name: eg: '杭州' 待搜索的区域, 多为省份, 城市, 具体区域
    :param page_num: start 1, 最大20
    :param page_size: 固定
    :param ip_pool_type:
    :param num_retries:
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    params = (
        ('query', str(keyword)),
        ('region', str(area_name)),
        ('output', 'json'),
        ('ak', str(ak)),
        ('page_num', str(page_num)),
        ('page_size', str(page_size)),
    )
    url = 'http://api.map.baidu.com/place/v2/search'
    body = Requests.get_url_body(
        url=url,
        headers=headers,
        params=params,
        use_proxy=use_proxy,
        ip_pool_type=ip_pool_type,
        num_retries=num_retries,
        timeout=timeout,)
    # print(body)
    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=logger,).get('results', [])
    # pprint(data)

    return data

def get_gd_map_shop_info_list_by_keyword_and_area_name(gd_key:str,
                                                       keyword:str,
                                                       area_name:str,
                                                       page_num: int,
                                                       page_size: int=20,
                                                       use_proxy=True,
                                                       ip_pool_type=tri_ip_pool,
                                                       num_retries=6,
                                                       timeout=20,
                                                       children=0,
                                                       extensions='all',
                                                       poi_type='',
                                                       logger=None,) -> list:
    """
    根据关键字和区域检索店铺信息(高德api 关键字搜索服务)
    :param gd_key: 申请的key
    :param keyword: 关键字 eg: '鞋子'
    :param area_name: eg: '杭州' 待搜索的区域, 城市名
    :param page_num: 最大翻页数100
    :param page_size: 默认值'20'
    :param use_proxy:
    :param ip_pool_type:
    :param num_retries:
    :param timeout:
    :param children: 按照层级展示子POI数据, 取值0 or 1
    :param extensions: 返回结果控制
    :param poi_type: 查询POI类型, eg: '061205', 可默认为空值!
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    params = (
        ('key', str(gd_key)),
        ('keywords', str(keyword)),
        ('types', str(poi_type)),
        ('city', str(area_name)),
        ('citylimit', 'true'),
        ('children', str(children)),
        ('offset', str(page_size)),
        ('page', str(page_num)),
        ('extensions', str(extensions)),
    )
    url = 'http://restapi.amap.com/v3/place/text'
    body = Requests.get_url_body(
        use_proxy=use_proxy,
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        timeout=timeout,
        num_retries=num_retries,)
    # print(body)
    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=logger,).get('pois', [])
    # pprint(data)

    return data

def get_gd_input_prompt_info(gd_key:str,
                             keyword,
                             city_name:str,
                             poi_type='',
                             lng:float=0.,
                             lat:float=0.,
                             ip_pool_type=tri_ip_pool,
                             num_retries=6,
                             timeout=20,
                             use_proxy=True,
                             logger=None,) -> list:
    """
    根据关键字和城市名获取输入提示(高德api)
    :param gd_key: 申请的key
    :param keyword: eg: '美食'
    :param city_name: eg: '杭州'
    :param poi_type: eg: '050301'
    :param lng:
    :param lat:
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    # eg: '116.481488,39.990464' 经纬度
    location = ','.join([str(lng), str(lat)]) if lng != 0. or lat != 0. else ''
    params = (
        ('key', str(gd_key)),
        ('keywords', str(keyword)),
        ('type', poi_type),
        ('location', location),
        ('city', str(city_name)),
        ('datatype', 'all'),
    )
    url= 'https://restapi.amap.com/v3/assistant/inputtips'
    body = Requests.get_url_body(
        use_proxy=use_proxy,
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        timeout=timeout,
        num_retries=num_retries,)
    # print(body)
    data = json_2_dict(
        json_str=body,
        logger=logger,).get('tips', [])
    # pprint(data)

    return data

def get_gd_reverse_geocode_info(gd_key:str,
                                address:str,
                                city_name:str,
                                ip_pool_type=tri_ip_pool,
                                num_retries=6,
                                timeout=20,
                                use_proxy=True,
                                logger=None,) -> list:
    """
    根据地址str获取逆向地理编码(高德api)
    :param gd_key:
    :param address: eg: '方恒国际中心A座'
    :param city_name: eg: '北京'
    :param ip_pool_type:
    :param num_retries:
    :param timeout:
    :param use_proxy:
    :param logger:
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    params = (
        ('key', str(gd_key)),
        ('address', str(address)),
        ('city', str(city_name)),
    )
    url= 'https://restapi.amap.com/v3/geocode/geo'
    body = Requests.get_url_body(
        use_proxy=use_proxy,
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        timeout=timeout,
        num_retries=num_retries,)
    # print(body)
    data = json_2_dict(
        json_str=body,
        logger=logger,).get('geocodes', [])
    # pprint(data)

    return data

def get_gd_map_shop_info_list_by_lng_and_lat_and_keyword(gd_key:str,
                                                         lng:float,
                                                         lat:float,
                                                         keyword:str='',
                                                         radius:int=1000,
                                                         page_num:int=1,
                                                         page_size:int=20,
                                                         poi_type='',
                                                         extensions='all',
                                                         use_proxy=True,
                                                         ip_pool_type=tri_ip_pool,
                                                         num_retries=6,
                                                         timeout=20,
                                                         logger=None,) -> list:
    """
    根据经纬度(主要根据), 关键字(附加条件)等条件检索附近店铺信息(高德api 关键字搜索服务)
    :param gd_key: 申请的key
    :param lng: 经度
    :param lat: 纬度
    :param keyword: 关键字 eg: '鞋子', 默认空值!
    :param radius: 半径 (如果已知的经纬度能准确定位到某家店铺, 可将radius=100, 来提高定位返回信息精确度!!)
    :param page_num: 最大翻页数100
    :param page_size: 默认值'20'
    :param poi_type: 查询POI类型, eg: '061205', 可默认为空值!
    :param extensions: 返回结果控制
    :param use_proxy:
    :param ip_pool_type:
    :param num_retries:
    :param timeout:
    :param logger:
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    params = (
        ('key', str(gd_key)),
        ('location', ','.join([str(lng), str(lat)])),
        ('keywords', str(keyword)),
        ('types', str(poi_type)),
        ('radius', str(radius)),
        ('offset', str(page_size)),
        ('page', str(page_num)),
        ('extensions', str(extensions)),
    )
    url = 'https://restapi.amap.com/v3/place/around'
    body = Requests.get_url_body(
        use_proxy=use_proxy,
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        timeout=timeout,
        num_retries=num_retries,)
    # print(body)
    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=logger,).get('pois', [])
    # pprint(data)

    return data

def get_gd_map_shop_info_list_by_gd_id(gd_key:str,
                                       gd_id:str,
                                       use_proxy=True,
                                       ip_pool_type=tri_ip_pool,
                                       num_retries=6,
                                       timeout=20,
                                       logger=None,) -> list:
    """
    根据gd_id来得到指定的shop info list(一般为第一个)[测试发现不准确, 根据id, 常返回不相干商家]
    :param gd_key: 申请的key
    :param gd_id: eg: 'B0FFIR6P0B'
    :param use_proxy:
    :param ip_pool_type:
    :param num_retries:
    :param timeout:
    :param logger:
    :return:
    """
    headers = get_base_headers()
    headers.update({
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    params = (
        ('id', gd_id),
        ('output', ''),
        ('key', gd_key),
    )
    url = 'https://restapi.amap.com/v3/place/detail'
    body = Requests.get_url_body(
        use_proxy=use_proxy,
        url=url,
        headers=headers,
        params=params,
        ip_pool_type=ip_pool_type,
        timeout=timeout,
        num_retries=num_retries,)
    # print(body)
    data = json_2_dict(
        json_str=body,
        default_res={},
        logger=logger,).get('pois', [])
    # pprint(data)

    return data
