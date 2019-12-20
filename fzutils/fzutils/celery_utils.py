# coding:utf-8

'''
@author = super_fazai
@File    : celery_utils.py
@connect : superonesfazai@gmail.com
'''

"""
celery常用函数
"""

import better_exceptions
better_exceptions.hook()

from time import time
from celery import Celery
from celery.utils.log import get_task_logger

from .common_utils import _print
from .time_utils import fz_set_timeout

__all__ = [
    'init_celery_app',                              # 初始化一个celery对象
    'block_get_celery_async_results',               # 同步得到celery worker的处理结果集合
    '_get_celery_async_results',                    # 得到celery worker的处理结果集合
    'get_current_all_celery_handled_results_list',  # 得到当前所有celery处理后子元素的子元素, 并以新集合形式返回!
]

DEFAULT_CELERY_ACCEPT_CONTENT = ['pickle', 'json']

def init_celery_app(name='proxy_tasks',
                    broker='redis://127.0.0.1:6379',
                    backend='redis://127.0.0.1:6379/0',
                    logger=None,
                    timezone='Asia/Shanghai',
                    task_acks_late=True,
                    accept_content=None,
                    task_serializer='pickle',
                    result_serializer='pickle',
                    celeryd_max_tasks_per_child=200,
                    result_expires=60*60,
                    task_soft_time_limit=None,
                    task_time_limit=None,
                    worker_log_color=True,) -> Celery:
    """
    初始化一个celery对象
    :param name: 创建一个celery实例, 名叫name
    :param broker: 指定消息中间件 格式: 'transport://userid:password@hostname:port/virtual_host'
    :param backend: 指定存储 格式同上
    :param logger: 最佳实践是在模块的顶层，为你的所有任务创建一个共用的logger
    :param timezone: 默认:'UTC', 配置Celery以使用自定义时区, 时区值可以是pytz支持的任何时区
    :param task_acks_late: 意味着任务消息将在任务执行后被确认，而不仅仅是在执行之前, 默认: False
    :param accept_content: 允许的内容类型/序列化的白名单, 默认: ['json',]
    :param task_serializer: 标识要使用的默认序列化方法的字符串(自4.0起:默认为'json', 早期为:'pickle')('pickle'是一种Python特有的自描述的数据编码, 可序列化自定义对象)
    :param result_serializer: 标识结果序列化的格式(自4.0起:默认为'json', 早期为:'pickle')
    :param celeryd_max_tasks_per_child: 表示每个工作的进程／线程／绿程 在执行 n 次任务后，主动销毁，之后会起一个新的。主要解决一些资源释放的问题。
    :param result_expires: 存储的任务结果在过期后会被删除, 单位s, 默认值: 1天
    :param task_soft_time_limit: 任务软时间限制, 单位s, celery执行任务时, 超过软时间限制, 就在任务中抛出SoftTimeLimitExceeded(from celery.exceptions import SoftTimeLimitExceeded)
    :param task_time_limit: 任务困难时间限制, 单位s, 处理任务的worker将被杀死并在超出此任务时替换为新任务, 实际在task运用: eg: @app.task(time_soft_limit=60, time_limit=120, rate_limit='200/m')
    :param worker_log_color: 启用/禁用Celery程序记录输出中的颜色, bool类型
    :return:
    """
    app = Celery(
        name,
        broker=broker,
        backend=backend,
        log=logger,)
    app.conf.update(
        CELERY_TIMEZONE=timezone,
        CELERY_ACKS_LATE=task_acks_late,
        CELERY_ACCEPT_CONTENT=DEFAULT_CELERY_ACCEPT_CONTENT if accept_content is None else accept_content,
        CELERY_TASK_SERIALIZER=task_serializer,
        CELERY_RESULT_SERIALIZER=result_serializer,
        CELERYD_FORCE_EXECV=True,
        # CELERYD_HIJACK_ROOT_LOGGER=False,                         # 想要用自己的logger, 则设置为False
        CELERYD_MAX_TASKS_PER_CHILD=celeryd_max_tasks_per_child,    # 长时间运行Celery有可能发生内存泄露，可以像下面这样设置, 这个表示每个工作的进程／线程／绿程 在执行 n 次任务后，主动销毁，之后会起一个新的。主要解决一些资源释放的问题。
        CELERY_TASK_RESULT_EXPIRES=result_expires,
        CELERYD_TASK_SOFT_TIME_LIMIT=task_soft_time_limit,
        CELERYD_TASK_TIME_LIMIT=task_time_limit,
        CELERYD_LOG_COLOR=worker_log_color,
        BROKER_HEARTBEAT=0,)

    return app

def block_get_celery_async_results(tasks:list, r_timeout=2.5, func_timeout=10 * 60) -> list:
    """
    得到celery worker的处理结果集合
    :param tasks: celery的tasks任务对象集
    :param r_timeout:
    :param func_timeout: 函数执行超时时间, 单位秒
    :return:
    """
    @fz_set_timeout(seconds=func_timeout)
    def get_res(tasks) -> list:
        """获取结果"""
        all = []
        success_num = 1
        while len(tasks) > 0:
            for r_index, r in enumerate(tasks):
                try:
                    if r.ready():
                        try:
                            all.append(r.get(timeout=r_timeout, propagate=False))
                            print('\r--->>> success_num: {}'.format(success_num), end='', flush=True)
                        except TimeoutError:
                            pass
                        success_num += 1
                        try:
                            tasks.pop(r_index)
                        except:
                            pass
                    else:
                        pass
                except Exception as e:
                    # redis.exceptions.TimeoutError: Timeout reading from socket
                    print(e)
                    return []
        else:
            pass

        return all

    s_time = time()
    try:
        all = get_res(tasks=tasks)
    except Exception as e:
        print(e)
        return []

    time_consume = time() - s_time
    print('\n执行完毕! 此次耗时 {} s!'.format(round(float(time_consume), 3)))

    return all

async def _get_celery_async_results(tasks:list, r_timeout=2.5, func_timeout=10 * 60) -> list:
    '''
    得到celery worker的处理结果集合
        该函数超时可用 from asyncio import wait_for as async_wait_for来处理协程超时, 并捕获后续异常!(超时后协程会被取消，导致无结果!!)
        eg:
            async def run():
                await async_sleep(3)

            # 原生超时
            try:
                res = await async_wait_for(run(), timeout=2)
            except AsyncTimeoutError as e:
                print(e)

        或者直接设置_get_celery_async_results 的func_timeout超时时长

    :param tasks: celery的tasks任务对象集
    :param r_timeout:
    :param func_timeout:
    :return:
    '''
    return block_get_celery_async_results(
        tasks=tasks,
        r_timeout=r_timeout,
        func_timeout=func_timeout,)

def get_current_all_celery_handled_results_list(one_res, logger=None) -> list:
    """
    得到当前所有celery处理后子元素的子元素, 并以新集合形式返回!
    :param one_res:
    :return:
    """
    res = []
    for i in one_res:
        try:
            for j in i:
                res.append(j)
        except TypeError as e:
            # _print(msg='遇到错误:', logger=logger, exception=e, log_level=2)
            continue

    return res
