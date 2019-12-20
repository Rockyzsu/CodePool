# coding:utf-8

'''
@author = super_fazai
@File    : memory_utils.py
@connect : superonesfazai@gmail.com
'''

"""
memory utils
"""

from pprint import pprint
from weakref import WeakKeyDictionary
from functools import wraps
from inspect import stack as inspect_stack
from traceback import extract_stack
from sys import _getframe as sys_getframe

from .common_utils import _print
# from fzutils.common_utils import _print

__all__ = [
    'memoizemethod_noargs',                                     # 使用一个方法缓存一个方法的结果（不带参数）弱引用对象
    'get_current_func_name',                                    # 获取当前被调用的函数名
    'get_current_func_info_by_traceback',                       # 通过traceback获取函数执行信息并打印
    'get_current_func_info_by_sys',                             # 通过sys获取执行信息并打印
]

def memoizemethod_noargs(method):
    '''
    使用一个方法缓存一个方法的结果（不带参数）弱引用对象
    :param method:
    :return:
    '''
    cache = WeakKeyDictionary()

    @wraps(method)
    def new_method(self, *args, **kwargs):
        if self not in cache:
            cache[self] = method(self, *args, **kwargs)

        return cache[self]

    return new_method

def get_current_func_name():
    """
    获取当前被调用的函数名
    eg:
    class MyClass:
        def function_one(self):
            print("%s.%s invoked" % (self.__class__.__name__, get_current_function_name()))
    a = MyClass()
    a.function_one()
    :return:
    """
    return inspect_stack()[1][3]

def get_current_func_info_by_traceback(self=None, logger=None) -> None:
    """
    通过traceback获取函数执行信息并打印
    use eg:
        class A:
            def a(self):
                def cc():
                    def dd():
                        get_current_func_info_by_traceback(self=self)
                    dd()
                cc()

        def b():
            get_current_func_info_by_traceback()

        aa = A()
        aa.a()
        b()
        # -> A.a.cc.dd in line_num: 131 invoked
        # -> <module>.b in line_num: 136 invoked
    :param self: 类的self
    :param logger:
    :return:
    """
    try:
        extract_stack_info = extract_stack()
        # pprint(extract_stack_info)
        # 除类名外的函数名调用组合str
        detail_func_invoked_info = ''
        for item in extract_stack_info[1:-1]:
            # extract_stack_info[1:-1]不包含get_current_func_info_by_traceback
            tmp_str = '{}' if detail_func_invoked_info == '' else '.{}'
            detail_func_invoked_info += tmp_str.format(item[2])
        # print(detail_func_invoked_info)

        # func_name = extract_stack_info[-2][2],
        line_num = extract_stack_info[-2][1]
        _print(msg='-> {}.{} in line_num: {} invoked'.format(
            # class name
            extract_stack_info[0][2] if self is None else self.__class__.__name__,
            detail_func_invoked_info,
            line_num,),
            logger=logger,
            log_level=1,)
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, exception=e, log_level=2)

    return None

def get_current_func_info_by_sys(logger=None) -> None:
    """
    通过sys获取执行信息并打印
    :param logger:
    :return:
    """
    now_frame = sys_getframe()
    _print(msg='-> file_path: {}, func_name: {} in line_num: {} invoked'.format(
        # 获取被调用函数所在模块文件名
        now_frame.f_code.co_filename,
        # 获取被调用函数名称
        now_frame.f_code.co_name,
        # 获取被调用函数在被调用时所处代码行数
        now_frame.f_back.f_lineno,),
        logger=logger,
        log_level=1,)

    return None