```bash
███████╗███████╗██╗   ██╗████████╗██╗██╗     ███████╗
██╔════╝╚══███╔╝██║   ██║╚══██╔══╝██║██║     ██╔════╝
█████╗    ███╔╝ ██║   ██║   ██║   ██║██║     ███████╗
██╔══╝   ███╔╝  ██║   ██║   ██║   ██║██║     ╚════██║
██║     ███████╗╚██████╔╝   ██║   ██║███████╗███████║
╚═╝     ╚══════╝ ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝                                                   
```
[![Build Status](https://travis-ci.org/EasyWeChat/site.svg?branch=master)](https://github.com/superonesfazai/fzutils)
[![GitHub license](https://img.shields.io/github/license/superonesfazai/fzutils.svg)](https://github.com/superonesfazai/fzutils/blob/master/LICENSE.txt)
[![GitHub forks](https://img.shields.io/github/forks/superonesfazai/fzutils.svg)](https://github.com/superonesfazai/fzutils/network)
[![GitHub stars](https://img.shields.io/github/stars/superonesfazai/fzutils.svg)](https://github.com/superonesfazai/fzutils/stargazers)
![](https://img.shields.io/github/issues/superonesfazai/fzutils.svg)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/superonesfazai/fzutils.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fsuperonesfazai%2Ffzutils)

# fzutils

## 这是什么?
这是fz的python utils包, for Spider.

旨在: 高效快速的进行爬虫开发的集成包

## Install
```bash
pip3 install fzutils
```

## 要求
-  Python 3或更高版本.
-  依靠的代理池(二选一)
    - [fz_ip_pool](https://github.com/superonesfazai/fz_ip_pools)
    - [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)

## simple use
```python
from fzutils.ip_pools import (
    IpPools,
    ip_proxy_pool,
    fz_ip_pool,)

# 高匿
# type默认是ip_proxy_pool, 可修改为fz_ip_pool, 具体看你使用哪个ip池
ip_obj = IpPools(type=ip_proxy_pool, high_conceal=True)     
# 得到一个随机ip, eg: 'http://175.6.2.174:8088'
proxy = ip_obj._get_random_proxy_ip()
```
```python
from fzutils.spider.crawler import Crawler, AsyncCrawler
from fzutils.ip_pools import fz_ip_pool

class ASpider(Crawler):     # Crawler为爬虫基类
    def __init__(self, logger=None) -> None:
        super(ASpider, self).__init__(
            ip_pool_type=fz_ip_pool,
            log_print=True,
            logger=logger,
            log_save_path='log文件存储path',
            
            is_use_driver=True,
            driver_executable_path='驱动path',
        )

class BSpider(AsyncCrawler):
    """异步爬虫"""
    pass

_ = ASpider()
```
```python
from fzutils.spider.fz_driver import BaseDriver, PHANTOMJS
from fzutils.ip_pools import ip_proxy_pool

# ip_pool_type默认也是ip_proxy_pool
# BaseDriver支持phantomjs, chromedriver, firefoxdriver
_ = BaseDriver(type=PHANTOMJS, executable_path='xxx', ip_pool_type=ip_proxy_pool)   
exec_code = '''
js = 'document.body.scrollTop=10000'
self.driver.execute_script(js) 
'''
body = _.get_url_body(url='xxx', exec_code=exec_code)
```
```python
from fzutils.spider.fz_requests import Requests
from fzutils.ip_pools import ip_proxy_pool

# ip_pool_type默认也是ip_proxy_pool
body = Requests.get_url_body(method='get', url='xxx', ip_pool_type=ip_proxy_pool)   
```
```python
import asyncio
from fzutils.spider.fz_aiohttp import AioHttp

async def tmp():
    _ = AioHttp(max_tasks=5)
    return await _.aio_get_url_body(url='xxx', headers={})
```
```python
from fzutils.time_utils import (
    fz_set_timeout,
    fz_timer,)
from time import sleep
import sys

# 设置执行超时
@fz_set_timeout(2)
def tmp():
    sleep(3)

# 计算函数用时, 支持sys.stdout.write or logger.info
@fz_timer(print_func=sys.stdout.write)
def tmp_2():
    sleep(3)
    
tmp()
tmp_2()
```
```python
from fzutils.log_utils import set_logger
from logging import INFO, ERROR

logger = set_logger(log_file_name='path', console_log_level=INFO, file_log_level=ERROR)
```
```python
from fzutils.auto_ops_utils import auto_git

# 自动化git
auto_git(path='xxx/path')
```
```python
from fzutils.path_utils import cd

# cd 到目标上下文并进行其他操作
with cd('path'):
    pass
```
```python
from fzutils.sql_utils import (
    BaseSqlServer,
    pretty_table,)

_ = BaseSqlServer(host='host', user='user', passwd='passwd', db='db', port='port')
# db美化打印
pretty_table(
    cursor=_._get_one_select_cursor(
        sql_str='sql_str', 
        params=('some_thing',)))
```
```python
from fzutils.linux_utils import (
    kill_process_by_name,
    process_exit,)

# 根据process_name kill process
kill_process_by_name(process_name='xxxx')
# 根据process_name 判断process是否存在
process_exit(process_name='xxxx')
```
```python
from fzutils.linux_utils import daemon_init

def run_forever():
    pass

# 守护进程
daemon_init()
run_forever()
```
```python
from fzutils.internet_utils import (
    get_random_pc_ua,
    get_random_phone_ua,)

# 随机user-agent
pc_user_agent = get_random_pc_ua()
phone_user_agent = get_random_phone_ua()
```
```python
from fzutils.common_utils import _print

# 支持sys.stdout.write or logger
_print(msg='xxx', logger=logger, exception=e, log_level=2)
```
```python
from fzutils.auto_ops_utils import (
    upload_or_download_files,
    local_compress_folders,
    remote_decompress_folders,)
from fabric.connection import Connection

connect_obj = Connection()
# local 与 server端 上传或下载文件
upload_or_download_files(
    method='put',
    connect_object=connect_obj,
    local_file_path='/Users/afa/myFiles/tmp/my_spider_logs.zip',
    remote_file_path='/root/myFiles/my_spider_logs.zip'
)
# 本地解压zip文件
local_compress_folders(
    father_folders_path='/Users/afa/myFiles',
    folders_name='my_spider_logs',
    default_save_path='xxxxxx'
)
# 远程解压zip文件
remote_decompress_folders(
    connect_object=connect_obj,
    folders_path='/root/myFiles/my_spider_logs.zip',
    target_decompress_path='/root/myFiles/'
)
```
```python
from fzutils.common_utils import json_2_dict

# json转dict, 处理部分不规范json
_dict = json_2_dict(json_str='json_str', logger=logger, encoding='utf-8')
```
```python
from fzutils.auto_ops_utils import judge_whether_file_exists
from fabric.connection import Connection

connect_obj = Connection()
# 判断server文件是否存在
result = judge_whether_file_exists(connect_object=connect_obj, file_path='file_path')
```
```python
from fzutils.email_utils import FZEmail

_ = FZEmail(user='xxx', passwd='密码 or smtp授权码')
_.send_email(to=['xxx@gmail.com',], subject='邮件正文', text='邮件内容')
```
```python
from requests import sessions
from fzutils.common_utils import (
    save_obj,
    get_obj,)

s = sessions()
# 对象持久化存储
save_obj(s, 's.txt')
get_obj('s.txt')
```
```python
from fzutils.data.str_utils import (
    char_is_chinese,
    char_is_alphabet,
    char_is_number,
    char_is_other,)

# 单字符判断其类型
print(char_is_chinese('你'))
print(char_is_alphabet('a'))
print(char_is_number('1'))
print(char_is_other('_'))
```
```python
from fzutils.algorithm_utils import merge_sort

# 归并排序
print(merge_sort([-1, 2, 1]))
# 还有很多其他排序方法
```
```python
from fzutils.data.pickle_utils import deserializate_pickle_object
from pickle import dumps

a = dumps({'1':1,})
# 反序列化python对象
print(deserializate_pickle_object(a))
```
```python
from fzutils.aio_utils import get_async_execute_result

# 获取异步执行结果
res = get_async_execute_result(obj='xxx类', obj_method_name='xxx类方法',)
```
```python
from fzutils.common_utils import retry

def validate_res(res):
    '''验证结果的函数'''
    if res == 5:
        return True
    else:
        return False

# 重试装饰器
@retry(max_retries=4, validate_func=validate_res)
def a(t):
    return t - 2

print(a(7))
```

### curl
curl cmd 转 python 代码
```python
from fzutils.curl_utils import curl_cmd_2_py_code

# 使用前提(已安装: npm install --save curlconverter)
curl_cmd = "curl 'http://en.wikipedia.org/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://www.wikipedia.org/' -H 'Cookie: GeoIP=US:Albuquerque:35.1241:-106.7675:v4; uls-previous-languages=%5B%22en%22%5D; mediaWiki.user.sessionId=VaHaeVW3m0ymvx9kacwshZIDkv8zgF9y; centralnotice_buckets_by_campaign=%7B%22C14_enUS_dsk_lw_FR%22%3A%7B%22val%22%3A%220%22%2C%22start%22%3A1412172000%2C%22end%22%3A1422576000%7D%2C%22C14_en5C_dec_dsk_FR%22%3A%7B%22val%22%3A3%2C%22start%22%3A1417514400%2C%22end%22%3A1425290400%7D%2C%22C14_en5C_bkup_dsk_FR%22%3A%7B%22val%22%3A1%2C%22start%22%3A1417428000%2C%22end%22%3A1425290400%7D%7D; centralnotice_bannercount_fr12=22; centralnotice_bannercount_fr12-wait=14' -H 'Connection: keep-alive' --compressed"
res = curl_cmd_2_py_code(curl_cmd)
```

### ocr识别
```python
from fzutils.ocr_utils import (
    baidu_ocr_captcha,
    baidu_orc_image_main_body,
    get_tracks_based_on_distance,
    dichotomy_match_gap_distance,)

# 百度orc识别captcha
captcah = baidu_ocr_captcha(
    app_id='xx', 
    api_key='xx', 
    secret_key='xx', 
    img_path='图片地址', 
    orc_type=2)
    
# 百度ocr识别图片主体内容位置
img_url = 'https://www.baidu.com/link?url=phUVHvSMIfwj2DPXnprj0BTv4loPocnLfNn-CVb7UQE4NLe7PH8GbrYKDkX2hzyp17Eqhy-s1rP8Zg92NEt0vqUxm_nhLoyRTaaxMFwq1oMdPaG_krazDsxHgLlql9QkZB92VhsTirtG53MvyecIFLjWeHjdyGCyTOaS-UcksfOJkPFOAJOFe4AoCxW5qQUbTahhjhjXWyihP-XmYIR5z-Gt3esBvFJpuHhUy7W6OODMrUZ2v7mUa9ng2BFKDy2MREyZQcXW80D3eDqWbIFLQ5BtEqWEknWa_1kxKXf4qo7GAZjkANyTP8D2PN0jHRw2AiWtN3d57J6GP4hksByVAzwIJWeWIiObv69Q1ekb2O_WsYLbKfzIsVLdlZGm5SHXnMgKZkRay_I8NKeq-wUb2wLKsGCjhRC1AV-GSv5Q7fIEj1QrSgQjLnW6Fjh55M5AaM9JRJLlXWhANegCn6jpJhnL7vcV1-kDgUcKQVFNq27fol2E2fG-d7ja03dizHCawAsIr6ortoWeqDdpyW4VOesI1VU6_WDdAWs96KZqVD2gATBs1U_D5nbYC9DAuZYK&wd=&eqid=81209347000143bf000000035b933e62'
res = baidu_orc_image_main_body(img_url=img_url)

# 根据给与距离生成仿生移动轨迹
tracks = get_tracks_based_on_distance(distance=100)

# 二分法匹配滑块与缺口间的距离
distance = dichotomy_match_gap_distance(bg_img_path='xxx', slide_img_path='xxx')
```

## qrcode
二维码解码
```python
from fzutils.qrcode_utils import decode_qrcode

img_url = 'https://i.loli.net/2018/11/15/5bed1adce184e.jpg'
print(decode_qrcode(img_url=img_url))
```

## 批量注册账号
```python
from pprint import pprint
from fzutils.register_utils import YiMaSmser

_ = YiMaSmser(username='账号', pwd='密码')
project_id = 715
while True:
    # 获取新手机号
    phone_num = _._get_phone_num(project_id=project_id)
    print(phone_num)
    a = input('是否可用: ')
    if a == 'y':
        break

print('\n未注册的: {}'.format(phone_num))
# 获取该手机号的短信
sms_res = _._get_sms(phone_num=phone_num, project_id=project_id)
print(sms_res)
# 查看自己的账户余额
money_res = _._get_account_info()
pprint(money_res)
```
```python
from time import time, sleep
from fzutils.register_utils import TwentyFourEmail

_ = TwentyFourEmail()
email_address = _._get_email_address()
print('获取到的email_address: {}'.format(email_address))
# # 换个邮箱
# email_address = _._get_new_email_address()
# print(email_address)
message_count = lambda : _._get_email_message_count()
start_time = time()
index = 1
while message_count() in (0, None) and time() - start_time < 100.:
    sleep_time = 2
    print('{} try, 休眠{}s...'.format(index, sleep_time))
    sleep(sleep_time)
    index += 1

message_list = _._get_email_message_list()
print(message_list)
```

### 代码模板生成
```python
from fzutils.spider.auto import auto_generate_crawler_code

# 爬虫基本代码自动生成器
auto_generate_crawler_code()
"""
shell输出如下: 
#--------------------------------
# 爬虫模板自动生成器 by super_fazai
#--------------------------------
@@ 下面是备选参数, 无输入则取默认值!!
请输入author:super_fazai
请输入email:superonesfazai@gmail.com
请输入创建的文件名(不含.py):fz_spider_demo
请输入class_name:FZSpiderDemo

创建爬虫文件fz_spider_demo.py完毕!
enjoy!🍺
"""
```
```python
# 还有很多其他常用函数, 待您探索...
```

## 资源
fzutils的home < https://www.github.com/superonesfazai/python >

## 版权和保修
此发行版中的代码为版权所有 (c) super_fazai, 除非另有明确说明.

fzutils根据MIT许可证提供, 包含的LICENSE文件详细描述了这一点.

## 贡献者
-  super_fazai

## 作者
super_fazai

<author_email: superonesfazai@gmail.com>

