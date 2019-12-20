# coding:utf-8

'''
@author = super_fazai
@File    : img_utils.py
@connect : superonesfazai@gmail.com
'''

"""
img utils
"""

from PIL import Image
import requests
from io import BytesIO
from base64 import b64encode

from .path_utils import from_file_path_get_file_extension_name
# from fzutils.path_utils import from_file_path_get_file_extension_name

__all__ = [
    'save_img_through_url',             # 根据img_url保存图片
    'read_img_use_base64',              # 以base64格式读取img

    # 截图
    'specified_position_screenshot',    # 对某图进行指定位置的块进行截图

    # 图片相似度
    'img_similarity_calculate',         # 获取图片相识度
]

def save_img_through_url(img_url, save_path) -> bool:
    '''
    根据img_url保存图片
    :param img_url:
    :param save_path:
    :return:
    '''
    res = False
    try:
        img = Image.open(BytesIO(requests.get(url=img_url).content))
        img.save(save_path)
        res = True
    except Exception as e:
        print(e)

    return res

def read_img_use_base64(file_path) -> bytes:
    '''
    以base64格式读取img
    :param file_path:
    :return:
    '''
    file_extension_name = from_file_path_get_file_extension_name(file_path=file_path)
    with open(file_path, 'rb') as f:
        img_content = bytes('data:image/{};base64,'.format(file_extension_name), encoding='utf-8') + b64encode(f.read())

        return img_content

def specified_position_screenshot(ori_img_path, target_img_save_path, left, top, right, bottom) -> bool:
    """
    对某图进行指定位置的块进行截图

        目标位置eg:
            selenium eg:
                获取验证码图片的x, y坐标, 及自身宽度和高度
                left = captcha.location['x']
                top = captcha.location['y']
                right = left + captcha.size['width']
                bottom = top +captcha.size['height']
            atx eg:
                bounds = d(className="android.view.View", instance=25).info.get('bounds', {})
                left, top, right, bottom = bounds.get('left'), bounds.get('top'), bounds.get('right'), bounds.get('bottom')
    :param ori_img_path: eg: '/Users/afa/myFiles/tmp/uiautomator2_files/screen'
    :param target_img_save_path: eg: '/Users/afa/myFiles/tmp/uiautomator2_files/screen'
    :param left:
    :param top:
    :param right:
    :param bottom:
    :return:
    """
    res = False
    try:
        img = Image.open(ori_img_path)
        target_img = img.crop((left, top, right, bottom))
        target_img.save(target_img_save_path)
        res = True
    except Exception as e:
        print(e)

    return res

def img_similarity_calculate(img_path1 , img_path2 , mode:int=3) -> (int, float):
    """
    获取图片相识度
    :param img_path1:
    :param img_path2:
    :param mode: 1 直方图的距离计算 | 2 直方图的距离计算 | 3 感知哈希算法 [不同的mode对应不同的类型]
    :return:
    """
    def img_difference(hist1, hist2):
        sum1 = 0
        for i in range(len(hist1)):
            if (hist1[i] == hist2[i]):
                sum1 += 1
            else:
                sum1 += 1 - float(abs(hist1[i] - hist2[i])) / max(hist1[i], hist2[i])

        return sum1 / len(hist1)

    # 预处理
    img1 = Image.open(img_path1).resize((256,256)).convert('RGB')
    img2 = Image.open(img_path2).resize((256,256)).convert('RGB')
    if mode == 1:
        return img_difference(img1.histogram(), img2.histogram())

    elif mode == 2:
        sum = 0
        for i in range(4):
            for j in range(4):
                hist1 = img1.crop((i*64, j*64, i*64+63, j*64+63)).copy().histogram()
                hist2 = img2.crop((i*64, j*64, i*64+63, j*64+63)).copy().histogram()
                sum += img_difference(hist1, hist2)
                # print(difference(hist1, hist2))
        return sum/16

    elif mode == 3:
        img1 = Image.open(img_path1).resize((8, 8)).convert('1')
        img2 = Image.open(img_path2).resize((8, 8)).convert('1')
        hist1 = list(img1.getdata())
        hist2 = list(img2.getdata())

        return img_difference(hist1, hist2)

    else:
        raise ValueError('mode值异常!')

