# coding:utf-8

'''
@author = super_fazai
@File    : qrcode_utils.py
@connect : superonesfazai@gmail.com
'''

"""
qrcode utils
"""

from requests import get
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode

__all__ = [
    'decode_qrcode',        # 二维码内容解码
]

def decode_qrcode(img_url=None, img_path=None, headers=None):
    '''
    二维码内容解码
    :param img_url: 二维码地址
    :param img_path: 本地图片路径
    :return:
    '''
    assert img_url is not None or img_path is not None, 'img_url or img_path都为None, 赋值异常!'
    # decode_result的格式是[Decoded(data='****',……)]，列表里包含一个name tuple
    if img_url is not None:
        decode_result = decode(Image.open(BytesIO(get(url=img_url, headers=headers).content)))
    elif img_path is not None:
        decode_result = decode(Image.open(img_path))
    else:
        raise AssertionError
    # print(decode_result)

    return str(decode_result[0].data, encoding='utf-8')

# img_path = './images/tmp.jpg'
# print(decode_qrcode(img_path=img_path))
# img_url = 'https://i.loli.net/2018/11/15/5bed1adce184e.jpg'
# print(decode_qrcode(img_url=img_url))