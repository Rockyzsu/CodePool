# coding:utf-8

# log utils

"""
切记: 不要重复创造日志对象，否则会重复打印
"""

# import os
from logging import (
    handlers,
    getLogger,)
from logging import Formatter as LoggingFormatter
from logging import StreamHandler as LoggingStreamHandler
from logging import FileHandler as LoggingFileHandler
from logging import ERROR as LOGGING_ERROR
from logging import DEBUG as LOGGING_DEBUG

__all__ = [
    'set_logger'
]

CONSOLE_FORMATTER = '%(asctime)s [%(levelname)-6s] ➞ %(message)s'
FILE_FORMATTER = '%(asctime)s [%(levelname)-6s] at %(filename)s 出错函数%(funcName)s.%(lineno)d ↴\n %(message)s\n'

def set_logger(log_file_name,
               console_log_level=LOGGING_DEBUG,
               file_log_level=LOGGING_ERROR,
               console_formatter=CONSOLE_FORMATTER,
               file_formatter=FILE_FORMATTER,
               logger_name='my_logger'):
    # 创建一个logger,可以考虑如何将它封装
    # 建议: 在有多个相互关联的文件都需要用到python的日志系统时，不要用默认的root logger。因为所有的名称都会继承root导致重复打印。用logger时一定要起名字！！
    logger = getLogger(logger_name)
    logger.setLevel(LOGGING_DEBUG)

    # 创建一个handler，用于写入日志文件
    # fh = LoggingFileHandler(os.path.join(os.getcwd(), './my_log.txt'))
    # 通过下面这句话就可以输出中文, encoding='utf-8'
    file_handler = handlers.RotatingFileHandler(
        filename=log_file_name,
        maxBytes=1024 * 1024,
        backupCount=5,
        encoding='utf-8',)

    file_handler.setLevel(file_log_level)

    # 再创建一个handler，用于输出到控制台
    console_handler = LoggingStreamHandler()
    console_handler.setLevel(console_log_level)

    # 定义handler的输出格式
    _console_formatter = LoggingFormatter(console_formatter)
    _file_formatter = LoggingFormatter(file_formatter)
    console_handler.setFormatter(_console_formatter)
    file_handler.setFormatter(_file_formatter)

    # 给logger添加handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 记录一条日志
    # logger.info('hello world, i\'m log helper in python, may i help you')

    return logger
