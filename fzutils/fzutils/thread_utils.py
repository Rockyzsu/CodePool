# coding:utf-8

'''
@author = super_fazai
@File    : thread_utils.py
@connect : superonesfazai@gmail.com
'''

"""
thread utils
"""

from functools import wraps
from pprint import pprint
from time import sleep
from threading import (
    Thread,
)
# Call a function after a specified number of seconds
from threading import Timer as ThreadTimer
# 用于控制线程数并发数
from threading import Semaphore as ThreadSemaphore
# 条件同步机制是指: 一个线程等待特定条件，而另一个线程发出特定条件满足的信号, 解释条件同步机制的一个很好的例子就是生产者/消费者（producer/consumer）模型
from threading import Condition as ThreadCondition
from threading import Event as ThreadEvent
from threading import enumerate as threading_enumerate

from .common_utils import _print

__all__ = [
    'thread_safe',                                      # 线程安全装饰器
    'ThreadTaskObj',                                    # 重写任务线程
    'start_thread_tasks_and_get_thread_tasks_res',      # 开启线程任务集合病获取目标任务集合所有执行结果
    'check_thread_tasks_and_restart',                   # 监控线程tasks状态, 挂掉的进行重启
]

def thread_safe(lock):
    """
    线程安全装饰器
    :param lock: 锁
    :return:
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper

    return decorate

class ThreadTaskObj(Thread):
    def __init__(self,
                 func_name,
                 args: (list, tuple)=(),
                 default_res=None,
                 func_timeout=None,
                 logger=None):
        """
        重写任务线程
        :param func_name:
        :param args:
        :param default_res:
        :param func_timeout: 超时时长, 单位秒
        :param logger:
        """
        super(ThreadTaskObj, self).__init__()
        self.func_name = func_name
        self.args = args
        # Thread默认结果
        self.default_res = default_res
        self.res = default_res
        self.func_timeout = func_timeout
        self.logger = logger

    def run(self):
        self.res = self.func_name(*self.args)

    def _get_result(self):
        try:
            # 等待线程执行完毕
            # Thread.join(self, timeout=self.func_timeout)
            # 改成下面
            self.join(timeout=self.func_timeout)
            return self.res
        except Exception as e:
            _print(
                msg='线程遇到错误:',
                logger=self.logger,
                log_level=2,
                exception=e)

            return self.default_res

def start_thread_tasks_and_get_thread_tasks_res(tasks: list, logger=None) -> list:
    """
    开启线程任务集合病获取目标任务集合所有执行结果
    simple use:
        def do_something(index):
            return 'xxx'

        tasks = []
        for index in range(1, 100):
            print('create task[where is index: {}] ...'.format(index))
            task = ThreadTaskObj(
                func_name=do_something,
                args=[
                    index,
                ],
                default_res=None,
                func_timeout=None,)
            tasks.append(task)
        one_res = start_thread_tasks_and_get_thread_tasks_res(tasks=tasks)

    :param tasks:
    :param logger:
    :return:
    """
    from time import time

    s_time = time()
    one_res = []
    try:
        _print(msg='请耐心等待所有任务完成...', logger=logger,)

        # 同时开启每个线程
        for task in tasks:
            try:
                task.start()
            except Exception as e:
                _print(
                    msg='开启线程出错:',
                    logger=logger,
                    log_level=2,
                    exception=e)
                continue

        # 获取所有线程的执行结果
        for task in tasks:
            res = task._get_result()
            one_res.append(res)
        # pprint(one_res)

        _print(msg='此次耗时 {} s!'.format(round(float(time() - s_time), 3)), logger=logger)

    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        return one_res

    return one_res

def check_thread_tasks_and_restart(need_to_be_monitored_thread_tasks_info_list: list,
                                   sleep_time=30,
                                   logger=None,):
    """
    监控线程tasks状态, 挂掉的进行重启
    simple use:

    def print_num(num):
        sleep(5.)
        print(num)

    class TestThread(Thread):
        def __init__(self, args: (list, tuple)=()):
            super(TestThread, self).__init__()
            self.args = args

        def run(self):
            sleep(5.)
            print(self.args[0])

    # 任务信息列表 eg: [{'thread_name': 'thread_task:print_ip:is_class_False:21113cf4-cc69-11e9-bdef-68fef70d1e6e', 'func_args': [xxx,]}, 'is_class': False]
    # 存储所有需要监控并重启的初始化线程对象list
    need_to_be_monitored_thread_tasks_info_list = []

    tasks = []
    # 函数类型的
    for num in range(0, 3):
        func_args = [
            num,
        ]
        t = Thread(
            target=print_num,
            args=func_args)
        thread_task_name = 'thread_task:{}:{}'.format(
            'print_ip',
            get_uuid1())
        t.setName(thread_task_name)
        tasks.append(t)
        need_to_be_monitored_thread_tasks_info_list.append({
            'func_name': print_num,
            'thread_name': thread_task_name,
            'func_args': func_args,
            'is_class': False,                  # 是否是类, 函数为False
        })

    # 继承自Thread的类
    for num in range(3, 4):
        func_args = [
            num,
        ]
        task = TestThread(args=func_args)
        thread_task_name = 'thread_task:{}:{}'.format(
            'TestThread',
            get_uuid1(),)
        task.setName(thread_task_name)
        tasks.append(task)
        need_to_be_monitored_thread_tasks_info_list.append({
            'func_name': TestThread,
            'thread_name': thread_task_name,
            'func_args': func_args,
            'is_class': True,
        })

    for t in tasks:
        t.start()

    # pprint(need_to_be_monitored_thread_tasks_info_list)

    # 用来检测是否有线程down并重启down线程
    check_thread_task = Thread(
        target=check_thread_tasks_and_restart,
        args=(
            need_to_be_monitored_thread_tasks_info_list,
            6,
        ))

    check_thread_task.setName('thread_task:check_thread_task_and_restart')
    check_thread_task.start()

    :param need_to_be_monitored_thread_tasks_info_list: 需要监控并重启的线程对象list, eg: [{'func_name': do_something, 'thread_name': 'thread_task:print_ip:21113cf4-cc69-11e9-bdef-68fef70d1e6e', 'func_args': [xxx,], 'is_class': False},], is_class为是否是类(继承自Thread)
    :param sleep_time:
    :param logger:
    :return:
    """
    while True:
        # 获取当前线程名list
        try:
            now_threads_name_list = [thread_obj.getName() for thread_obj in threading_enumerate()]
            # pprint(now_threads_name_list)
        except Exception as e:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
            continue

        for thread_obj_info in need_to_be_monitored_thread_tasks_info_list:
            thread_name = thread_obj_info['thread_name']
            func_args = thread_obj_info['func_args']
            func_name = thread_obj_info['func_name']
            is_class = thread_obj_info['is_class']
            # _print(msg='thread_name: {}'.format(thread_name), logger=logger)

            if  thread_name in now_threads_name_list:
                # 当前某线程名包含在初始化线程组中，可以认为线程仍在运行
                continue
            else:
                _print(
                    msg='thread_name: {} stopped, now restart!'.format(thread_name),
                    logger=logger,)
                # 报错: RuntimeError: threads can only be started once
                # 每个线程对象只能运行一次, 所以每次得重新thread_obj = Thread()线程对象, 然后thread_obj.start()
                # 因此必须把相关运行参数传进来
                if not is_class:
                    thread_task = Thread(
                        target=func_name,
                        name=thread_name,
                        args=func_args,)

                else:
                    # print(func_name)
                    # 此处继承自类的格式必须为
                    """
                    eg:
                    class TestThread(Thread):
                        def __init__(self, args: (list, tuple) = ()):
                            super(TestThread, self).__init__()
                            self.args = args

                        def run(self):
                            pass
                    """
                    thread_task = func_name(args=func_args)
                    thread_task.setName(name=thread_name)

                thread_task.start()

        sleep(sleep_time)