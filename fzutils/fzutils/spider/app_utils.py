# coding:utf-8

'''
@author = super_fazai
@File    : app_utils.py
@connect : superonesfazai@gmail.com
'''

"""
app utils
"""

import better_exceptions
better_exceptions.hook()

from gc import collect
from random import uniform
from asyncio import get_event_loop
from pprint import pprint
from time import sleep

from ..common_utils import _print
from ..spider.async_always import async_sleep
from ..aio_utils import async_wait_tasks_finished

__all__ = [
    # atx
    'u2_block_page_back',                           # [阻塞]u2的页面返回
    'u2_page_back',                                 # u2的页面返回
    'u2_get_device_display_h_and_w',                # u2获取设备的高跟宽
    'u2_get_some_ele_height',                       # u2得到某一个ele块的height
    'u2_block_up_swipe_some_height',                # [阻塞]u2 上滑某个高度
    'u2_up_swipe_some_height',                      # u2上滑某个高度
    'async_get_u2_ele_info',                        # 异步获取u2 ele 的info
    'AndroidDeviceObj',                             # 设备信息类
    'get_u2_init_device_list',                      # 得到初始化u2设备对象list
    'u2_get_device_obj_by_device_id',               # [阻塞]根据device_id初始化获取到device_obj
    'u2_unblock_get_device_obj_by_device_id',       # [异步非阻塞]根据device_id初始化获取到device_obj
    'u2_get_ui_obj',                                # u2获取指定UI元素对象(因为用u2编码时没有参数提示)

    # mitmproxy
    'get_mitm_flow_request_headers_user_agent',     # 获取flow.request.headers的user_agent
]

# 上滑
U2_SLIDE_UP = 'up'
# 下滑
U2_SLIDE_DOWN = 'down'
# 左滑
U2_SLIDE_LEFT = 'left'
# 右滑
U2_SLIDE_RIGHT = 'right'

def u2_block_page_back(d, back_num=1):
    """
    [阻塞]u2的页面返回
    :param d:
    :param back_num:
    :return:
    """
    while back_num > 0:
        d.press('back')
        back_num -= 1
        sleep(.3)

    return

async def u2_page_back(d, back_num=1):
    """
    u2的页面返回
    :param d: eg: u2 d
    :param back_num:
    :return:
    """
    return u2_block_page_back(
        d=d,
        back_num=back_num,)

async def u2_get_device_display_h_and_w(d) -> tuple:
    """
    u2获取设备的高跟宽
    :param d: eg: u2 d
    :return:
    """
    device_height = d.device_info.get('display', {}).get('height')
    device_width = d.device_info.get('display', {}).get('width')

    return device_height, device_width

async def u2_get_some_ele_height(ele):
    """
    u2得到某一个ele块的height
    :param ele: eg: d(resourceId="com.taobao.taobao:id/topLayout")
    :return:
    """
    return ele.info.get('bounds', {}).get('bottom') \
           - ele.info.get('bounds', {}).get('top')

def u2_block_up_swipe_some_height(d, swipe_height, base_height=.1) -> None:
    """
    [阻塞]u2 上滑某个高度
    :param d:
    :param swipe_height:
    :param base_height:
    :return:
    """
    d.swipe(0., base_height + swipe_height, 0., base_height)

async def u2_up_swipe_some_height(d, swipe_height, base_height=.1) -> None:
    """
    u2 上滑某个高度
    :param d:
    :param height:
    :param base_height:
    :return:
    """
    return u2_block_up_swipe_some_height(
        d=d,
        swipe_height=swipe_height,
        base_height=base_height,)

async def async_get_u2_ele_info(ele, logger=None) -> tuple:
    """
    异步获取ele 的info
    :param ele: UiObject [from uiautomator2.session import UiObject]
    :return: (ele, ele_info)
    """
    async def _get_args() -> list:
        '''获取args'''
        return [
            ele,
        ]

    def _get_ele_info(ele) -> dict:
        return ele.info

    loop = get_event_loop()
    args = await _get_args()
    ele_info = {}
    try:
        ele_info = await loop.run_in_executor(None, _get_ele_info, *args)
        # print('*' * 50)
        # print(ele_info)
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
    finally:
        # loop.close()
        try:
            del loop
        except:
            pass
        _print(
            msg='[{}] ele: {}'.format('+' if ele_info != {} else '-', ele),
            logger=logger,)
        collect()

        return ele, ele_info

def get_mitm_flow_request_headers_user_agent(headers, logger=None) -> str:
    """
    获取flow.request.headers的user_agent
    :param headers: flow.request.headers obj
    :return:
    """
    user_agent = ''
    try:
        headers = dict(headers)
        # pprint(headers)
        for key, value in headers.items():
            if key == 'user-agent':
                user_agent = value
                break
            else:
                continue
        assert user_agent != '', 'user_agent不为空str!'
    except Exception as e:
        _print(
            msg='遇到错误',
            logger=logger,
            exception=e,
            log_level=2)

    return user_agent

class AndroidDeviceObj(object):
    """设备信息类"""
    def __init__(self, d, device_id: str, device_product_name: str):
        """
        init
        :param d: UIAutomatorServer类的对象[from uiautomator2 import UIAutomatorServer]
        :param device_id: 设备唯一id
        :param device_product_name: 设备名称 eg: d.info.get('productName', '')来获得
        """
        self.d = d
        self.device_id = device_id
        self.device_product_name = device_product_name

def u2_get_device_obj_by_device_id(u2,
                                   device_id: str,
                                   pkg_name: str='',
                                   open_someone_pkg=True,
                                   d_debug: bool = False,
                                   set_fast_input_ime=True,
                                   logger=None):
    """
    [阻塞]根据device_id初始化获取到device_obj
    :param u2: import uiautomator2 as u2的u2
    :param device_id:
    :param pkg_name: APP包名
    :param open_someone_pkg: bool 初始化设备时是否打开指定pkg_name
    :param d_debug: 是否为debug模式
    :param set_fast_input_ime:
    :param logger:
    :return:
    """
    _print(msg='init device_id: {} ...'.format(device_id), logger=logger)
    # 设置设备id
    d = u2.connect(addr=device_id)
    d_info = d.info
    _print(msg='{}'.format(d_info), logger=logger)
    device_product_name = d_info.get('productName', '')
    assert device_product_name != '', 'device_product_name !=""'
    d.set_fastinput_ime(set_fast_input_ime)
    d.debug = d_debug

    if open_someone_pkg and pkg_name != '':
        # 启动指定包
        now_session = d.session(pkg_name=pkg_name)

    device_obj = AndroidDeviceObj(
        d=d,
        device_id=device_id,
        device_product_name=device_product_name,)
    _print(msg='init device_id: {} over !'.format(device_id), logger=logger)

    return device_obj

async def u2_unblock_get_device_obj_by_device_id(u2,
                                                 device_id: str,
                                                 pkg_name: str='',
                                                 open_someone_pkg=True,
                                                 d_debug: bool = False,
                                                 set_fast_input_ime=True,
                                                 logger=None):
    """
    [异步非阻塞]根据device_id初始化获取到device_obj
    :param u2: import uiautomator2 as u2的u2
    :param device_id:
    :param pkg_name:
    :param open_someone_pkg: bool 初始化设备时是否打开指定pkg_name
    :param d_debug:
    :param set_fast_input_ime:
    :param logger:
    :return:
    """
    async def _get_args() -> list:
        """获取args"""
        return [
            u2,
            device_id,
            pkg_name,
            open_someone_pkg,
            d_debug,
            set_fast_input_ime,
            logger,
        ]

    loop = get_event_loop()
    args = await _get_args()
    device_obj = None
    try:
        device_obj = await loop.run_in_executor(None, u2_get_device_obj_by_device_id, *args)
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
    finally:
        # loop.close()
        try:
            del loop
        except:
            pass
        collect()

        return device_obj

async def get_u2_init_device_list(loop,
                                  u2,
                                  device_id_list:list,
                                  pkg_name: str = '',
                                  open_someone_pkg=True,
                                  d_debug=False,
                                  set_fast_input_ime=True,
                                  logger=None) -> list:
    """
    得到初始化u2设备对象list
    :param loop:
    :param u2: import uiautomator2 as u2的u2
    :param device_id_list: eg: ['816QECTK24ND8', ...]
    :param pkg_name: app 包名
    :param open_someone_pkg: bool 初始化设备时是否打开指定pkg_name
    :param d_debug: u2 是否为调试模式
    :param set_fast_input_ime:
    :param logger:
    :return:
    """
    device_obj_list = []
    tasks = []
    for device_id in device_id_list:
        tasks.append(loop.create_task(u2_unblock_get_device_obj_by_device_id(
            u2=u2,
            device_id=device_id,
            pkg_name=pkg_name,
            open_someone_pkg=open_someone_pkg,
            d_debug=d_debug,
            set_fast_input_ime=set_fast_input_ime,
            logger=logger,)))

    all_res = await async_wait_tasks_finished(tasks=tasks)
    # pprint(all_res)
    for device_obj in all_res:
        device_obj_list.append(device_obj)

    try:
        del tasks
    except:
        pass

    return device_obj_list

def human_swipe(d,
                slide_distance:(int, float),
                slide_direction=U2_SLIDE_UP,
                base_distance=.1,
                x_or_y_no_slip_begin=.1,
                x_or_y_no_slip_end=.2):
    """
    模拟人类滑动
    :param d:
    :param slide_distance: 滑动的距离
    :param slide_direction: 滑动的方向
    :param base_distance:
    :param x_or_y_no_slip_begin: 不滑动方向的随机最小值
    :param x_or_y_no_slip_end: 不滑动方向的随机最大值
    :return:
    """
    if slide_direction == U2_SLIDE_UP:
        # 上滑
        x0 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        x1 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        d.swipe(x0, base_distance + slide_distance, x1, base_distance)

    elif slide_direction == U2_SLIDE_DOWN:
        # 下滑
        x0 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        x1 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        d.swipe(x0, base_distance, x1, base_distance + slide_distance)

    elif slide_direction == U2_SLIDE_LEFT:
        # 左滑
        assert base_distance > slide_distance, 'base_distance > slide_distance'
        y0 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        y1 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        d.swipe(base_distance-slide_distance, y0, base_distance, y1)

    elif slide_direction == U2_SLIDE_RIGHT:
        # 右滑
        y0 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        y1 = uniform(x_or_y_no_slip_begin, x_or_y_no_slip_end)
        d.swipe(base_distance, y0, base_distance + slide_distance, y1)

    else:
        raise ValueError('slide_direction value 异常!')

def u2_get_ui_obj(d,
                  resourceId=None,
                  resourceIdMatches=None,
                  text=None,
                  textContains=None,
                  textMatches=None,
                  textStartsWith=None,
                  className=None,
                  classNameMatches=None,
                  description=None,
                  descriptionContains=None,
                  descriptionMatches=None,
                  descriptionStartsWith=None,
                  packageName=None,
                  packageNameMatches=None,
                  checkable:bool=False,
                  checked:bool=False,
                  clickable:bool=False,
                  longClickable:bool=False,
                  scrollable:bool=False,
                  enabled:bool=False,
                  focusable:bool=False,
                  focused:bool=False,
                  selected:bool=False,
                  index:int=0,
                  instance:int=0,):
    """
    u2获取指定UI元素对象(因为用u2编码时没有参数提示)
        note: (参数默认值可从 from uiautomator2.session import Selector查看)
    :return: UiObject (from uiautomator2.session import UiObject) eg: ele: UiObject = u2_get_ui_obj(d=d, resourceId='xxxx') 来调用后续方法
    """
    # 必须进行对应的相面判断再赋值
    # 因为u2的UiObject中接收的selector如果某参数为默认值是不进行传值的
    # 否则报错: java.lang.IllegalStateException: Checkable selector is already defined
    # 其源码地址: https://android.googlesource.com/platform/frameworks/uiautomator/+/android-support-test/src/main/java/android/support/test/uiautomator/BySelector.java
    # TODO 不传值则 mCheckable == null, 不会抛出异常!
    # public BySelector checkable(boolean isCheckable) {
    #     if (mCheckable != null) {
    #         throw new IllegalStateException("Checkable selector is already defined");
    #     }
    #     mCheckable = isCheckable;
    #     return this;
    # }

    kwargs = {}
    if resourceId is not None:
        kwargs.update({
            'resourceId': resourceId,
        })
    if resourceIdMatches is not None:
        kwargs.update({
            'resourceIdMatches': resourceIdMatches,
        })
    if text is not None:
        kwargs.update({
            'text': text,
        })
    if textContains is not None:
        kwargs.update({
            'textContains': textContains,
        })
    if textMatches is not None:
        kwargs.update({
            'textMatches': textMatches,
        })
    if textStartsWith is not None:
        kwargs.update({
            'textStartsWith': textStartsWith,
        })
    if className is not None:
        kwargs.update({
            'className': className,
        })
    if classNameMatches is not None:
        kwargs.update({
            'classNameMatches': classNameMatches,
        })
    if description is not None:
        kwargs.update({
            'description': description,
        })
    if descriptionContains is not None:
        kwargs.update({
            'descriptionContains': descriptionContains,
        })
    if descriptionMatches is not None:
        kwargs.update({
            'descriptionMatches': descriptionMatches,
        })
    if descriptionStartsWith is not None:
        kwargs.update({
            'descriptionStartsWith': descriptionStartsWith,
        })
    if packageName is not None:
        kwargs.update({
            'packageName': packageName,
        })
    if packageNameMatches is not None:
        kwargs.update({
            'packageNameMatches': packageNameMatches,
        })

    if checkable:
        kwargs.update({
            'checkable': checkable,
        })
    if checked:
        kwargs.update({
            'checked': checked,
        })
    if clickable:
        kwargs.update({
            'clickable': clickable,
        })
    if longClickable:
        kwargs.update({
            'longClickable': longClickable,
        })
    if scrollable:
        kwargs.update({
            'scrollable': scrollable,
        })
    if enabled:
        kwargs.update({
            'enabled': enabled,
        })
    if focusable:
        kwargs.update({
            'focusable': focusable,
        })
    if focused:
        kwargs.update({
            'focused': focused,
        })
    if selected:
        kwargs.update({
            'selected': selected,
        })

    if index != 0:
        kwargs.update({
            'index': index,
        })
    if instance != 0:
        kwargs.update({
            'instance': instance,
        })

    return d(**kwargs)

