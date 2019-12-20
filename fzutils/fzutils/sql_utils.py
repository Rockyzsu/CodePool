# coding:utf-8

'''
@author = super_fazai
@File    : sql_utils.py
@Time    : 2016/7/14 14:36
@connect : superonesfazai@gmail.com
'''

"""
sql utils
"""

import better_exceptions
better_exceptions.hook()

from gc import collect
import sqlite3
# from pymssql import *
from pymssql import connect as pymssql_connect
from pymssql import IntegrityError
from time import sleep
from redis import (
    ConnectionPool,
    StrictRedis,)
from pickle import dumps as pickle_dumps

from .common_utils import _print

__all__ = [
    'BaseSqlServer',                        # cli for sql_server
    'BaseRedisCli',                         # cli for redis
    'BaseSqlite3Cli',                       # cli for sqlite3
    'pretty_table',                         # 美化打印table
    'create_dcs_tasks_in_redis',            # 根据target_list创建分布式任务并插入到redis
]

class BaseSqlServer(object):
    """
    sql_utils for sql_server
    """
    def __init__(self, host, user, passwd, db, port):
        super(BaseSqlServer, self).__init__()
        # 死锁重试次数
        self.dead_lock_retry_num = 3
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self._init_conn()

    def _init_conn(self):
        self.is_connect_success = True
        try:
            self.conn = pymssql_connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.db,
                port=self.port,
                charset='utf8')
        except Exception:
            self.is_connect_success = False
            print('数据库连接失败!!')

    def _select_table(self,
                      sql_str,
                      params=None,
                      lock_timeout=20000,
                      logger=None,):
        res = None
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass

            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                log_level=2,
                exception=e,)
            return res

        try:
            # 设置隔离级别为脏读
            cs.execute('set tran isolation level read uncommitted;')
            cs.execute('set lock_timeout {0};'.format(lock_timeout))  # 设置客户端执行超时等待为20秒
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                cs.execute(sql_str, params)
            else:
                cs.execute(sql_str)
            # self.conn.commit()
            res = cs.fetchall()
        except Exception as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                log_level=2,
                exception=e,)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return res

    def _insert_into_table(self,
                           sql_str,
                           params: tuple,
                           repeat_insert_default_res: bool=None) -> bool:
        """
        插入表数据
        :param sql_str:
        :param params:
        :param repeat_insert_default_res: 控制重复插入的返回值, 默认None, 返回True
        :return:
        """
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(msg='遇到错误:', exception=e,)
            return _

        try:
            cs.execute('set deadlock_priority low;')        # 设置死锁释放级别
            cs.execute(sql_str.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            print('[+] add to db!')
            _ = True
        except IntegrityError:
            print('重复插入...')
            if repeat_insert_default_res is None:
                _ = True
            else:
                _ = repeat_insert_default_res

        except Exception as e:
            print('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
            _print(
                msg='遇到错误:',
                exception=e,)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def _insert_into_table_2(self,
                             sql_str,
                             params: tuple,
                             logger,
                             set_deadlock_priority_low=True,
                             repeat_insert_default_res: bool=None) -> bool:
        """
        :param sql_str:
        :param params:
        :param logger:
        :param set_deadlock_priority_low: 是否设置死锁等级低
        :param repeat_insert_default_res: 控制重复插入的返回值, 默认None, 返回True
        :return:
        """
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                log_level=2,
                exception=e, )
            return _

        try:
            if set_deadlock_priority_low:
                cs.execute('set deadlock_priority low;')  # 设置死锁释放级别

            # logger.info(str(params))
            cs.execute(sql_str.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            logger.info('[+] add to db!')
            _ = True
        except IntegrityError:
            logger.info('重复插入goods_id[%s], 此处跳过!' % params[0])
            if repeat_insert_default_res is None:
                _ = True
            else:
                _ = repeat_insert_default_res
        except Exception:
            logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: %s' % params[0], exc_info=True)
        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    async def _insert_into_table_3(self,
                                   sql_str,
                                   params: tuple,
                                   logger,
                                   error_msg_dict=None,
                                   repeat_insert_default_res: bool=None) -> bool:
        """
        异步
            error_msg_dict参数:
                eg: {
                    # 重复插入
                    'repeat_error': {
                        'field_name': '重复插入要记录的字段名',
                        'field_value': '重复记录该字段的值',
                    },
                    # 其他异常
                    'other_error': [{
                        'field_name': '字段名',
                        'field_value': '字段值',
                    }, ...]
                }
        :param sql_str:
        :param params:
        :param logger:
        :param error_msg_dict: logger记录的额外信息
        :param repeat_insert_default_res: 控制重复插入的返回值, 默认None, 返回True
        :return:
        """
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                log_level=2,
                exception=e, )
            return _

        try:
            cs.execute('set deadlock_priority low;')  # 设置死锁释放级别
            # logger.info(str(params))
            cs.execute(sql_str.encode('utf-8'), params)  # 注意必须是tuple类型
            self.conn.commit()
            logger.info('[+] add to db!')
            _ = True
        except IntegrityError:
            if repeat_insert_default_res is None:
                _ = True
            else:
                _ = repeat_insert_default_res
            if not error_msg_dict:
                logger.info('重复插入goods_id[%s], 此处跳过!' % params[0])
            else:
                if isinstance(error_msg_dict, dict):
                    msg = '重复插入{0}[{1}], 此处跳过!'.format(
                        error_msg_dict.get('repeat_error', {}).get('field_name', ''),
                        error_msg_dict.get('repeat_error', {}).get('field_value', '')
                    )
                    logger.info(msg)
                else:
                    raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')

        except Exception:
            if not error_msg_dict:
                logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: {0}'.format(params[0]), exc_info=True)
            else:
                if isinstance(error_msg_dict, dict):
                    msg = '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | '
                    for item in error_msg_dict.get('other_error', []):
                        msg += '出错{0}: {1} '.format(
                            item.get('field_name', ''),
                            item.get('field_value', '')
                        )
                    logger.error(msg, exc_info=True)
                else:
                    raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')

        finally:
            try:
                cs.close()
            except Exception:
                pass
            return _

    def _update_table(self, sql_str, params: tuple) -> bool:
        """
        更新表数据
        :param sql_str:
        :param params:
        :return:
        """
        ERROR_NUMBER = 0
        RETRY_NUM = self.dead_lock_retry_num    # 死锁重试次数
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(msg='遇到错误:', exception=e,)
            return _

        while RETRY_NUM > 0:
            try:
                cs.execute('set deadlock_priority low;')    # 设置死锁释放级别
                cs.execute(sql_str, params)
                self.conn.commit()        # 不进行事务提交, 不提交无法更改
                print('[+] add to db!')
                _ = True
                RETRY_NUM = 0
            except Exception as e:
                try:
                    ERROR_NUMBER = e.number
                except:
                    pass
                if ERROR_NUMBER == 1025:  # 死锁状态码
                    print('遇到死锁!!进入等待...')
                    sleep(1)
                    RETRY_NUM -= 1
                else:
                    print('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 |')
                    print('--------------------| 错误如下: ', e)
                    RETRY_NUM = 0

            finally:
                try:
                    cs.close()
                except Exception:
                    pass

        return _

    def _update_table_2(self, sql_str, params: tuple, logger) -> bool:
        ERROR_NUMBER = 0
        # 死锁重试次数
        RETRY_NUM = self.dead_lock_retry_num
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                log_level=2,
                exception=e, )
            return _

        while RETRY_NUM > 0:
            try:
                # 设置死锁释放级别
                cs.execute('set deadlock_priority low;')
                cs.execute(sql_str, params)
                self.conn.commit()        # 不进行事务提交
                logger.info('[+] add to db!')
                _ = True
                RETRY_NUM = 0
            except Exception as e:
                try:
                    ERROR_NUMBER = e.number
                except:
                    pass
                if ERROR_NUMBER == 1025:
                    # 死锁状态码
                    logger.error('遇到死锁!!进入等待...')
                    sleep(1)
                    RETRY_NUM -= 1
                else:
                    logger.error('| 修改信息失败, 未能将该页面信息存入到sqlserver中 出错goods_id: %s|' % params[-1])
                    logger.exception(e)
                    RETRY_NUM = 0

            finally:
                try:
                    cs.close()
                except Exception:
                    pass

        return _

    async def _update_table_3(self, sql_str, params: tuple, logger, error_msg_dict=None) -> bool:
        """
        异步更新数据
            error_msg_dict参数:
                eg: {
                    # 其他异常
                    'other_error': [{
                        'field_name': '字段名',
                        'field_value': '字段值',
                    }, ...]
                }
        :param sql_str:
        :param params:
        :param logger:
        :param error_msg_dict: logger记录的额外信息
        :return:
        """
        ERROR_NUMBER = 0
        # 死锁重试次数
        RETRY_NUM = self.dead_lock_retry_num
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                logger=logger,
                log_level=2,
                exception=e,)
            return _

        while RETRY_NUM > 0:
            try:
                # 设置死锁释放级别
                cs.execute('set deadlock_priority low;')
                cs.execute(sql_str, params)
                self.conn.commit()
                logger.info('[+] add to db!')
                _ = True
                RETRY_NUM = 0
            except Exception as e:
                try:
                    ERROR_NUMBER = e.number
                except:
                    pass
                if ERROR_NUMBER == 1025:
                    # 死锁状态码
                    sleep(1)
                    RETRY_NUM -= 1
                    logger.error('遇到死锁!!进入等待...')
                else:
                    RETRY_NUM = 0
                    if not error_msg_dict:
                        logger.error('-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | 出错goods_id: {0}'.format(params[-1]), exc_info=True)
                    else:
                        if isinstance(error_msg_dict, dict):
                            msg = '-' * 9 + '| 修改信息失败, 未能将该页面信息存入到sqlserver中 | '
                            for item in error_msg_dict.get('other_error', []):
                                msg += '出错{0}: {1} '.format(
                                    item.get('field_name', ''),
                                    item.get('field_value', '')
                                )
                            logger.error(msg, exc_info=True)

                        else:
                            raise TypeError('传入的error_msg_dict类型错误, 请核对需求参数!')
            finally:
                try:
                    cs.close()
                except Exception:
                    pass

        return _

    def _delete_table(self, sql_str, params=None, lock_timeout=20000) -> bool:
        _ = False
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cs = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                exception=e, )
            return _

        try:
            # 设置客户端执行超时等待为20秒
            cs.execute('set lock_timeout {0};'.format(lock_timeout))
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                cs.execute(sql_str, params)
            else:
                cs.execute(sql_str)
            self.conn.commit()        # 不进行事务提交
            _ = True
        except Exception as e:
            _print(
                msg='遇到错误:',
                exception=e,)
        finally:
            try:
                cs.close()
            except Exception:
                pass

            return _
    
    def _get_one_select_cursor(self, sql_str, params=None, lock_timeout=20000):
        """
        获得一个select执行结果的cursor(用于美化打印table)
        :return: 查询失败 None | 成功的cursor
        """
        cursor = None
        try:
            if not self.is_connect_success:
                raise AssertionError('sql_server连接失败! 执行操作终止!')
            else:
                pass
            cursor = self.conn.cursor()
        except (AttributeError, AssertionError) as e:
            _print(
                msg='遇到错误:',
                exception=e,)
            return cursor

        try:
            cursor.execute('set lock_timeout {0};'.format(lock_timeout))  # 设置客户端执行超时等待为20秒
            if params is not None:
                if not isinstance(params, tuple):
                    params = tuple(params)
                cursor.execute(sql_str, params)
            else:
                cursor.execute(sql_str)
        except Exception as e:
            _print(
                msg='遇到错误:',
                exception=e,)
            cursor = None

            return cursor

        return cursor
    
    def __del__(self):
        try:
            if self.is_connect_success:
                # 连接成功才进行释放
                self.conn.close()
            else:
                pass
            del self.is_connect_success
            del self.host
            del self.user
            del self.passwd
            del self.db
            del self.port
        except Exception:
            pass
        try:
            collect()
        except Exception:
            pass

def pretty_table(cursor):
    '''
    美化打印table返回的数据(只支持select)
    :param cursor: cursor数据库的游标
    :return: None
    '''
    from prettytable import from_db_cursor

    tb = from_db_cursor(cursor=cursor)   # 返回一个 PrettyTable对象
    tb.align = 'l'  # 左对齐
    # tb.padding_width = 5
    print(tb)

    return

class BaseRedisCli():
    '''redis客户端'''
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.pool = ConnectionPool(
            host=host,
            port=port,
            db=db,)
        self.redis_cli = StrictRedis(connection_pool=self.pool)

    def set(self, name, value):
        '''写/改'''
        return self.redis_cli.set(name=name, value=value)

    def get(self, name):
        '''读'''
        return self.redis_cli.get(name=name)

    def delete(self, name):
        '''删'''
        return self.redis_cli.delete(name)

    def __del__(self):
        try:
            del self.pool
            del self.redis_cli
        except:
            pass
        collect()

def create_dcs_tasks_in_redis(redis_pool,
                              spider_name: str,
                              target_list: (list, tuple),
                              base_name='fzhook',
                              task_serializer: str='pickle',
                              key_expire: (float, int) = 60 * 60,
                              nx: bool = True,
                              decode_responses: bool=False,
                              encoding='utf-8',
                              max_connections=None,
                              logger=None,) -> None:
    """
    根据target_list创建分布式任务并插入到redis
    :param redis_pool: from redis import ConnectionPool as RedisConnectionPool 实例对象
    :param spider_name: 爬虫名
    :param target_list: eg: [{'unique_id': 'xxx', 'value': 'xxxx',}, ...]
    :param base_name:
    :param task_serializer: 任务序列化方式 支持: 'pickle'
    :param key_expire: 单位秒, 默认60分钟
    :param nx: bool True 只有name不存在时, 当前set操作才执行
    :param decode_responses: False 以二进制编码 True 以字符串, 默认二进制, encoding='utf-8'
    :param encoding:
    :param max_connections:
    :return:
    """
    try:
        redis_cli = StrictRedis(
            connection_pool=redis_pool,
            decode_responses=decode_responses,
            encoding=encoding,
            max_connections=max_connections,)
    except Exception as e:
        _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
        return None

    for item in target_list:
        try:
            unique_id = item.get('unique_id', '')
            assert unique_id != ''
            value = item.get('value')
            assert value is not None

            if task_serializer == 'pickle':
                # value = pickle_dumps(value)
                # 避免取出时报错: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte
                # 存入时: Python对象 -> 字节串 -> latin字符串 -> utf8字节串存储在Redis里
                # 取出时: utf8字节串 -> 解码变成字符串 -> 通过latin1编码成字节串 -> Python对象
                # eg: pickle.loads(r.get(sid).encode('latin1'))
                value = pickle_dumps(value).decode('latin1')
            else:
                raise ValueError('task_serializer value 异常!')

            name = '{base_name}:{spider_name}:{unique_id}'.format(
                base_name=base_name,
                spider_name=spider_name,
                unique_id=unique_id,)
            _print(msg='insert name: {} ...'.format(name), logger=logger)
            redis_cli.set(
                name=name,
                value=value,
                ex=key_expire,
                # 只有name不存在时, 当前set操作才执行
                nx=nx,)
        except (AssertionError, Exception) as e:
            _print(msg='遇到错误:', logger=logger, log_level=2, exception=e)
            continue

    return None

class BaseSqlite3Cli(object):
    """
    sqlite3 obj
        always use:
            1. 查看db中所有表: select name from sqlite_master where type='table' order by name;
    """
    def __init__(self, db_path):
        self.conn = sqlite3.connect(database=db_path)

    def _execute(self, sql_str, params:(dict, tuple)=None) -> sqlite3.Cursor:
        '''
        执行(结果可根据相应db操作查看结果)(切记游标每次用完close())
        :param sql_str:
        :param params:
        :return:
        '''
        cursor = self.conn.cursor()
        try:
            if params is None:
                cursor.execute(sql_str)
            else:
                cursor.execute(sql_str, params)
            self.conn.commit()
        except Exception as e:
            print(e)

        return cursor

    def __del__(self):
        try:
            del self.conn
        except:
            pass
        collect()
