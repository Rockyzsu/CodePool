# coding:utf-8

'''
@author = super_fazai
@File    : my_exceptions.py
@connect : superonesfazai@gmail.com
'''

import better_exceptions
from sys import exc_info
from traceback import format_tb

from .common_utils import _print

__all__ = [
    'ResponseBodyIsNullStrException',       # 请求的应答返回的body为空str异常, 多用于处理proxy异常中, 避免数据误删
    'NoNextPageException',                  # 没有后续页面的异常
    'AppNoResponseException',               # app 长期运行, 无响应异常!
    'catch_exceptions',                     # 异常捕获装饰器(适用于常规函数, 不适用于协程函数)
    'catch_exceptions_with_class_logger',   # 类logger异常捕获装饰器(适用于类函数, 不适用于类协程函数)
]

class ResponseBodyIsNullStrException(Exception):
    """请求的应答返回的body为空str异常, 多用于处理proxy异常中, 避免数据误删"""
    pass

class NoNextPageException(Exception):
    """没有后续页面的异常"""
    pass

class AppNoResponseException(Exception):
    """app 长期运行, 无响应异常!"""
    pass

def catch_exceptions(logger=None, default_res=None):
    """
    异常捕获装饰器(只适用于常规函数, 不适用于协程函数)
        simple use:
            @catch_exceptions(default_res='test')
            def test():
                assert '1' != ''

            res = test()
            print(res)
    :param logger:
    :param default_res:
    :return:
    """
    def decorator(func):
        nonlocal logger, default_res
        def handle_problems(*args, **kwargs):
            nonlocal logger, default_res
            try:
                default_res = func(*args, **kwargs)
            except Exception:
                try:
                    exc_type, exc_instance, exc_traceback = exc_info()
                    formatted_traceback = ''.join(format_tb(exc_traceback))
                    message = '\n{0}\n{1}: {2}'.format(
                        formatted_traceback,
                        exc_type.__name__,
                        exc_instance,)
                    # raise exc_type(message)

                    # 放置此处进行异常优化捕获
                    better_exceptions.hook()
                    # print(logger)
                    if logger is None:
                        print(exc_type(message))
                    else:
                        logger.error('遇到错误:', exc_info=True)

                except Exception as e:
                    _print(
                        msg='遇到错误:',
                        logger=logger,
                        log_level=2,
                        exception=e,)

                # 其他你喜欢的操作
            finally:
                return default_res

        return handle_problems

    return decorator

def catch_exceptions_with_class_logger(default_res=None):
    """
    类logger异常捕获装饰器(适用于类函数, 不适用于类协程函数)
        simple use:
            class Test:
                def __init__():
                    self.lg = xxx

                @catch_exceptions_with_class_logger(default_res='test')
                def test():
                    assert '1' != ''

            res = Test().test()
            print(res)
    :param logger:
    :param default_res:
    :return:
    """
    def decorator(func):
        nonlocal default_res
        def handle_problems(self, *args, **kwargs):
            nonlocal default_res
            # print(self.lg)
            try:
                default_res = func(self, *args, **kwargs)
            except Exception:
                try:
                    # 异常类型, 异常说明, 发生异常的traceback
                    exc_type, exc_instance, exc_traceback = exc_info()
                    formatted_traceback = ''.join(format_tb(exc_traceback))
                    message = '\n{0}\n{1}: {2}'.format(
                        formatted_traceback,
                        exc_type.__name__,
                        exc_instance,)
                    # raise exc_type(message)

                    # 放置此处进行异常优化捕获
                    better_exceptions.hook()
                    self.lg.error('遇到错误:', exc_info=True)
                    # 其他你喜欢的操作
                except Exception as e:
                    _print(
                        msg='遇到错误:',
                        logger=self.lg,
                        log_level=2,
                        exception=e)

            finally:
                return default_res

        return handle_problems

    return decorator
