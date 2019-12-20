# coding:utf-8

"""
aio 异步utils
"""

from gc import collect
from asyncio import (
    get_event_loop,
    wait,
    iscoroutinefunction,
    new_event_loop,
    set_event_loop,
)
from gevent import spawn as gevent_spawn
from gevent import monkey as gevent_monkey

from pprint import pprint
from scrapy.selector import Selector

from .thread_utils import (
    ThreadTaskObj,
    start_thread_tasks_and_get_thread_tasks_res,
)
from .gevent_utils import (
    wait_for_every_greenlet_obj_run_over_and_get_tasks_res,
)
from .twisted_utils import (
    twisted_reactor,
    twisted_defer,
    twisted_threads,
    twisted_threadable,
    handle_deferred_list_res,
)
from .ip_pools import (
    ip_proxy_pool,
    fz_ip_pool,
    tri_ip_pool,
)
from .spider.fz_aiohttp import AioHttp
from .common_utils import _print
from .spider.fz_requests import (
    Requests,
    PROXY_TYPE_HTTP,
    PROXY_TYPE_HTTPS,)
from .internet_utils import get_base_headers
from .spider.fz_phantomjs import PHANTOMJS_DRIVER_PATH
from .spider.fz_driver import (
    BaseDriver,
    PC,
    PHANTOMJS,
)

__all__ = [
    'Asyncer',
    'get_async_execute_result',                         # 获取异步执行结果
    'async_wait_tasks_finished',                        # 异步等待目标tasks完成
    'TasksParamsListObj',                               # 任务参数List
    'unblock_request',                                  # 非阻塞的request请求
    'unblock_get_driver_obj',                           # 异步获取driver obj
    'unblock_request_by_driver',                        # 非阻塞的request by driver
    'unblock_func',                                     # 异步函数非阻塞
    'default_add_one_res_2_all_res',                    # 默认函数1: one_res 增加到all_res
    'default_add_one_res_2_all_res2',                   # 默认函数2: one_res 增加到all_res
    'get_or_handle_target_data_by_task_params_list',    # 根据task_params_list并发 获取 or 处理 所有目标数据
    'start_bg_loop',                                    # 开启一个在后台永远运行的事件循环(多用于主线程与子线程并行执行)
]

class Asyncer(object):
    """异步类"""
    async def get_async_requests_body(**kwargs):
        return await AioHttp.aio_get_url_body(**kwargs)

def get_async_execute_result(obj=Asyncer,
                             obj_method_name='get_async_requests_body',
                             **kwargs):
    """
    获取异步执行结果
    :param obj: 对象的类
    :param obj_method_name: 对象的方法名
    :param kwargs: 该方法附带的参数
    :return:
    """
    loop = get_event_loop()
    if hasattr(obj, obj_method_name):
        method_callback = getattr(obj, obj_method_name)
    else:
        raise AttributeError('{obj}类没有{obj_method_name}方法!'.format(obj=obj, obj_method_name=obj_method_name))

    result = loop.run_until_complete(
        future=method_callback(**kwargs))

    return result

async def async_wait_tasks_finished(tasks:list) -> list:
    """
    异步等待目标tasks完成
    :param tasks: 任务集
    :return:
    """
    from time import time

    s_time = time()
    try:
        print('请耐心等待所有任务完成...')
        success_jobs, fail_jobs = await wait(tasks)
        print('执行完毕! success_task_num: {}, fail_task_num: {}'.format(len(success_jobs), len(fail_jobs)))
        time_consume = time() - s_time
        print('此次耗时 {} s!'.format(round(float(time_consume), 3)))
        all_res = [r.result() for r in success_jobs]
    except Exception as e:
        print(e)
        return []

    return all_res

class TasksParamsListObj(object):
    """
    任务参数List
        simple use:
            a = [1,2,3,4,5]
            _ = TasksParamsListObj(tasks_params_list=a, step=2)
            while True:
                try:
                    print(_.__next__())
                except AssertionError as e:
                    break
    """
    def __init__(self, tasks_params_list, step, slice_start_index=0):
        """
        :param tasks_params_list: tasks 的参数list
        :param step: 步长，即并发量
        :param slice_start_index: 切片起始位置
        """
        self.tasks_params_list = tasks_params_list
        self.tasks_params_list_len = len(tasks_params_list)
        self.step = step
        self.slice_start_index = slice_start_index

    def __next__(self):
        assert self.slice_start_index < self.tasks_params_list_len, '超出长度!'

        res = self.tasks_params_list[self.slice_start_index:self.step+self.slice_start_index]
        self.slice_start_index += self.step
        # print(self.slice_start_index)

        return res

    def __del__(self):
        try:
            del self.tasks_params_list
        except:
            pass
        collect()

async def unblock_request(url,
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
                          proxy_type=PROXY_TYPE_HTTP,
                          logger=None,
                          is_new_loop=False,) -> str:
    """
    非阻塞的request请求
    :param url:
    :param use_proxy:
    :param headers:
    :param params:
    :param data:
    :param cookies:
    :param had_referer:
    :param encoding:
    :param method:
    :param timeout:
    :param num_retries:
    :param high_conceal:
    :param ip_pool_type:
    :param verify:
    :param _session:
    :param get_session:
    :param proxies:
    :param proxy_type:
    :param logger:
    :param is_new_loop:
    :return:
    """
    func_args = [
        url,
        use_proxy,
        headers,
        params,
        data,
        cookies,
        had_referer,
        encoding,
        method,
        timeout,
        num_retries,
        high_conceal,
        ip_pool_type,
        verify,
        _session,
        get_session,
        proxies,
        proxy_type,
    ]
    body = await unblock_func(
        func_name=Requests.get_url_body,
        func_args=func_args,
        logger=logger,
        default_res='',
        is_new_loop=is_new_loop,)

    return body

async def unblock_get_driver_obj(type=PHANTOMJS,
                                 load_images=False,
                                 executable_path=PHANTOMJS_DRIVER_PATH,
                                 logger=None,
                                 high_conceal=True,
                                 headless=False,
                                 driver_use_proxy=True,
                                 user_agent_type=PC,
                                 driver_obj=None,
                                 ip_pool_type=ip_proxy_pool,
                                 extension_path=None,
                                 driver_cookies=None,
                                 chrome_enable_automation=False,
                                 is_new_loop=False,):
    """
    异步获取一个driver obj
    :return:
    """
    func_args = [
        type,
        load_images,
        executable_path,
        logger,
        high_conceal,
        headless,
        driver_use_proxy,
        user_agent_type,
        driver_obj,
        ip_pool_type,
        extension_path,
        driver_cookies,
        chrome_enable_automation,
    ]
    driver_obj = await unblock_func(
        func_name=BaseDriver,
        func_args=func_args,
        logger=logger,
        default_res=None,
        is_new_loop=is_new_loop,)

    return driver_obj

async def unblock_request_by_driver(url,
                                    type=PHANTOMJS,
                                    load_images=False,
                                    executable_path=PHANTOMJS_DRIVER_PATH,
                                    logger=None,
                                    high_conceal=True,
                                    headless=False,
                                    driver_use_proxy=True,
                                    user_agent_type=PC,
                                    driver_obj=None,
                                    ip_pool_type=ip_proxy_pool,
                                    extension_path=None,
                                    driver_cookies=None,

                                    css_selector='',
                                    exec_code='',
                                    timeout=20,
                                    change_proxy: bool=False,
                                    change_user_agent: bool=False,

                                    is_new_loop=False,) -> str:
    """
    非阻塞的driver 的请求
    :param url:
    :param type:
    :param load_images:
    :param executable_path:
    :param logger:
    :param high_conceal:
    :param headless:
    :param driver_use_proxy:
    :param user_agent_type:
    :param driver_obj:
    :param ip_pool_type:
    :param extension_path:
    :param driver_cookies:
    :param css_selector:
    :param exec_code:
    :param timeout:
    :param change_proxy:
    :param change_user_agent:
    :param is_new_loop:
    :return:
    """
    driver = await unblock_get_driver_obj(
        type=type,
        load_images=load_images,
        executable_path=executable_path,
        logger=logger,
        high_conceal=high_conceal,
        headless=headless,
        driver_use_proxy=driver_use_proxy,
        user_agent_type=user_agent_type,
        driver_obj=driver_obj,
        ip_pool_type=ip_pool_type,
        extension_path=extension_path,
        driver_cookies=driver_cookies,)
    func_args = [
        url,
        css_selector,
        exec_code,
        timeout,
        change_proxy,
        change_user_agent,
    ]
    body = ''
    try:
        body = await unblock_func(
            func_name=driver.get_url_body,
            func_args=func_args,
            logger=logger,
            default_res='',
            is_new_loop=is_new_loop,)
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
    finally:
        # loop.close()
        try:
            del driver
        except:
            pass
        collect()

        return body

async def unblock_func(func_name:object,
                       func_args,
                       logger=None,
                       default_res=None,
                       is_new_loop=False,):
    """
    异步函数非阻塞
    :param func_name: def 函数对象名
    :param func_args: 请求参数可迭代对象(必须遵循元素入参顺序!)
    :param logger:
    :param default_res: 默认返回结果
    :param is_new_loop: 是否开启新loop, True容易造成OSError, too many file open错误
    :return:
    """
    # todo notice: 一个进程/线程只能一个 event loop
    loop = get_event_loop() if not is_new_loop else new_event_loop()
    try:
        default_res = await loop.run_in_executor(None, func_name, *func_args)
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
    finally:
        # loop.close()
        try:
            del loop
        except:
            pass
        collect()

        return default_res

def default_add_one_res_2_all_res(one_res: list, all_res: list) -> list:
    """
    默认函数1: one_res 增加到all_res
    :param one_res:
    :param all_res:
    :return:
    """
    for i in one_res:
        for j in i:
            all_res.append(j)

    return all_res

def default_add_one_res_2_all_res2(one_res: list, all_res: list) -> list:
    """
    默认函数2: one_res 增加到all_res
    :param one_res:
    :param all_res:
    :return:
    """
    for i in one_res:
        all_res.append(i)

    return all_res

async def get_or_handle_target_data_by_task_params_list(loop,
                                                        tasks_params_list: list,
                                                        func_name_where_get_create_task_msg,
                                                        func_name: object,
                                                        func_name_where_get_now_args,
                                                        func_name_where_handle_one_res=None,
                                                        func_name_where_add_one_res_2_all_res=default_add_one_res_2_all_res,
                                                        one_default_res=None,
                                                        is_new_loop: bool=False,
                                                        step: int = 10,
                                                        slice_start_index: int=0,
                                                        logger=None,
                                                        get_all_res=True,
                                                        concurrent_type: int=0,
                                                        # thread
                                                        func_timeout=None,
                                                        # gevent
                                                        gevent_joinall_timeout=None,
                                                        gevent_joinall_raise_error: bool=True,
                                                        gevent_joinall_count=None,
                                                        # twisted
                                                        twisted_with_threads=1,
                                                        fire_on_one_callback: bool=False,
                                                        fire_on_one_errback: bool=False,
                                                        consume_errors: bool=False,
                                                        deferred_list_timeout=None,
                                                        deferred_list_clock=None,
                                                        deferred_list_callback_func_args: (list, tuple)=(),) -> list:
    """
    根据task_params_list并发 获取 or 处理 所有目标数据
    :param tasks_params_list:
    :param func_name_where_get_create_task_msg:     (多用闭包形式) or eg: def get_create_task_msg(self, k) -> str: return 'create task[where page_num: {}]...'.format(k['page_num'])
    :param func_name:                               阻塞函数名
    :param func_name_where_get_now_args:            (多用闭包形式) or eg: def get_now_args(self, k) -> list: return [k['page_num'],]
    :param func_name_where_handle_one_res:          数据量较大时处理用于单独处理one_res
    :param func_name_where_add_one_res_2_all_res:   根据需求处理one_res到all_res中
    :param one_default_res:                         单个task 出现异常时, 返回的默认参数
    :param is_new_loop:                             unblock_func是否为新loop, True容易造成OSError, too many file open错误
    :param step:                                    并发量 eg: step=self.concurrency
    :param slice_start_index:
    :param logger:
    :param get_all_res:                             bool 是否获取所有结果, 默认获取
    :param concurrent_type:                         并发的类型: 0 协程 | 1 线程 | 2 gevent | 3 twisted
    :param func_timeout:                            线程模式下的函数超时, 单位秒
    :param gevent_joinall_timeout:
    :param gevent_joinall_raise_error:
    :param gevent_joinall_count:
    :param twisted_with_threads:                    默认1即可
    :param fire_on_one_callback:
    :param fire_on_one_errback:
    :param consume_errors:
    :param deferred_list_timeout:                   延迟列表超时
    :param deferred_list_clock:
    :param deferred_list_callback_func_args:        增加回调函数参数: list
    :return:
    """
    assert concurrent_type in [0, 1, 2, 3], 'concurrent_type value异常!'

    # todo 不可放在执行时导monkey
    # 报错: gevent.exceptions.LoopExit: This operation would block forever
    # 解决方案: 在脚本的导包处的最下端, 进行concurrent_type == 2判断, 相等则gevent_monkey.patch_all() else pass
    # if concurrent_type == 2:
    #     gevent_monkey.patch_all()
    # else:
    #     pass

    all_res = []
    tasks_params_list_obj = TasksParamsListObj(
        tasks_params_list=tasks_params_list,
        step=step,
        slice_start_index=slice_start_index, )
    while True:
        try:
            slice_params_list = tasks_params_list_obj.__next__()
        except AssertionError:
            break

        tasks = []
        for k in slice_params_list:
            _print(
                msg=func_name_where_get_create_task_msg(k=k),
                logger=logger, )

            if concurrent_type == 0:
                tasks.append(loop.create_task(unblock_func(
                    func_name=func_name,
                    func_args=func_name_where_get_now_args(k=k),
                    logger=logger,
                    default_res=one_default_res,
                    is_new_loop=is_new_loop, )))

            elif concurrent_type == 1:
                tasks.append(ThreadTaskObj(
                    func_name=func_name,
                    args=func_name_where_get_now_args(k=k),
                    logger=logger,
                    default_res=one_default_res,
                    func_timeout=func_timeout, ))

            elif concurrent_type == 2:
                # notice 无法设置func_name执行的异常默认值, 需func_name中进行补货设置异常默认值
                func_args = func_name_where_get_now_args(k=k)
                tasks.append(gevent_spawn(
                    func_name,
                    *func_args,
                ))

            elif concurrent_type == 3:
                # notice 无法设置func_name执行的异常默认值, 需func_name中进行补货设置异常默认值
                func_args = func_name_where_get_now_args(k=k)
                tasks.append(twisted_threads.deferToThread(
                    func_name,
                    *func_args,
                ))

            else:
                continue

        one_res = []
        if concurrent_type == 0:
            one_res = await async_wait_tasks_finished(tasks=tasks)
        elif concurrent_type == 1:
            one_res = start_thread_tasks_and_get_thread_tasks_res(
                tasks=tasks,
                logger=logger,)
        elif concurrent_type == 2:
            one_res = wait_for_every_greenlet_obj_run_over_and_get_tasks_res(
                tasks=tasks,
                gevent_joinall_timeout=gevent_joinall_timeout,
                gevent_joinall_raise_error=gevent_joinall_raise_error,
                gevent_joinall_count=gevent_joinall_count,
                logger=logger, )
        elif concurrent_type == 3:
            def get_twisted_deferred_list_res(*args) -> list:
                """
                获取延迟列表deferred_list执行结果
                :param args: tuple
                :return:
                """
                nonlocal deferred_list_res
                # pprint(args)
                deferred_list_res = list(args)

                return deferred_list_res

            from time import time

            try:
                s_time = time()
                # 延迟列表
                deferred_list = twisted_defer.DeferredList(
                    deferredList=tasks,
                    fireOnOneCallback=fire_on_one_callback,
                    fireOnOneErrback=fire_on_one_errback,
                    consumeErrors=consume_errors, )
                deferred_list_res = []
                if deferred_list_clock is not None \
                        and deferred_list_timeout is not None:
                    # 设置超时
                    deferred_list.addTimeout(
                        timeout=deferred_list_timeout,
                        clock=deferred_list_clock, )
                else:
                    pass

                deferred_list \
                    .addCallback(
                    callback=get_twisted_deferred_list_res,
                    *deferred_list_callback_func_args, ) \
                    .addCallback(
                    # 停止
                    callback=lambda x: twisted_reactor.stop())

                twisted_threadable.init(with_threads=twisted_with_threads)
                # 启动
                twisted_reactor.run()
                one_res = handle_deferred_list_res(
                    deferred_list_res=deferred_list_res)
                _print(
                    msg='此次耗时 {} s!'.format(round(float(time() - s_time), 3)),
                    logger=logger, )

            except Exception as e:
                _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
                return one_res

        else:
            pass
        # pprint(one_res)
        if func_name_where_handle_one_res is not None:
            # 执行需要处理one_res函数
            if iscoroutinefunction(func_name_where_handle_one_res):
                # _print(msg='函数为协程函数!', logger=logger)
                await func_name_where_handle_one_res(one_res=one_res)
            else:
                func_name_where_handle_one_res(one_res=one_res)
        else:
            pass

        if get_all_res:
            all_res = func_name_where_add_one_res_2_all_res(
                one_res=one_res,
                all_res=all_res)
        else:
            pass
        try:
            del tasks
            del one_res
        except:
            pass
        collect()

    try:
        del tasks_params_list_obj
    except:
        pass
    collect()

    return all_res

def start_bg_loop(loop):
    """
    开启一个在后台永远运行的事件循环(多用于主线程与子线程并行执行)
    :param loop:
    :return:
    """
    set_event_loop(loop)
    loop.run_forever()