## ajaxcrawl

```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import logging

import six
from w3lib import html

from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse


logger = logging.getLogger(__name__)
````
这些也是导入几个包， 主要看下第一个absolute_import
```cmd
关于这句from __future__ import absolute_import的作用: 
直观地看就是说”加入绝对引入这个新特性”。说到绝对引入，当然就会想到相对引入。那么什么是相对引入呢?比如说，你的包结构是这样的: 
pkg/ 
pkg/init.py 
pkg/main.py 
pkg/string.py

如果你在main.py中写import string,那么在Python 2.4或之前, Python会先查找当前目录下有没有string.py, 若找到了，则引入该模块，然后你在main.py中可以直接用string了。如果你是真的想用同目录下的string.py那就好，但是如果你是想用系统自带的标准string.py呢？那其实没有什么好的简洁的方式可以忽略掉同目录的string.py而引入系统自带的标准string.py。这时候你就需要from __future__ import absolute_import了。这样，你就可以用import string来引入系统的标准string.py, 而用from pkg import string来引入当前目录下的string.py了
```

### 构造函数
```python
   def __init__(self, settings):
        if not settings.getbool('AJAXCRAWL_ENABLED'):
            raise NotConfigured

        # XXX: Google parses at least first 100k bytes; scrapy's redirect
        # middleware parses first 4k. 4k turns out to be insufficient
        # for this middleware, and parsing 100k could be slow.
        # We use something in between (32K) by default.
        self.lookup_bytes = settings.getint('AJAXCRAWL_MAXSIZE', 32768)
```
我们可以看出， 先从设置中获取AJAXCTRAWL_ENABLED是否启用， 如果没有设置，就抛出一个没有配置的异常
设置获取AJAXCRAWL_MAXSIZE ,提供默认值32768

### from_crawler方法
```python
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
```
这个方法，就是根据一个crawler抓取者去构造一个ajaxcrawl中间件

### process_response方法
```python
    def process_response(self, request, response, spider):

        if not isinstance(response, HtmlResponse) or response.status != 200:
            return response

        if request.method != 'GET':
            # other HTTP methods are either not safe or don't have a body
            return response

        if 'ajax_crawlable' in request.meta:  # prevent loops
            return response

        if not self._has_ajax_crawlable_variant(response):
            return response

        # scrapy already handles #! links properly
        ajax_crawl_request = request.replace(url=request.url+'#!')
        logger.debug("Downloading AJAX crawlable %(ajax_crawl_request)s instead of %(request)s",
                     {'ajax_crawl_request': ajax_crawl_request, 'request': request},
                     extra={'spider': spider})

        ajax_crawl_request.meta['ajax_crawlable'] = True
        return ajax_crawl_request
```
这段代码先判断response不HtmlResponse响应流或者状态码不是200就直接返回响应流，如果请求方法不是get也直接返回，如果在request.meta中有ajax_crawlable就直接返回，如果响应流中没有ajax可抓取的变量也是直接返回，构造请求，请求的url为原来的url+“#!”
### _has_ajax_crawlable_variant
```python
    def _has_ajax_crawlable_variant(self, response):
        """
        Return True if a page without hash fragment could be "AJAX crawlable"
        according to https://developers.google.com/webmasters/ajax-crawling/docs/getting-started.
        """
        body = response.text[:self.lookup_bytes]
        return _has_ajaxcrawlable_meta(body)
```
这个方法就是判断下系那个应留是否有ajax可以提取的信息

### 变量定义
```python
_ajax_crawlable_re = re.compile(six.u(r'<meta\s+name=["\']fragment["\']\s+content=["\']!["\']/?>'))
```
### _has_ajaxcrawlable_meta
```python 
def _has_ajaxcrawlable_meta(text):
    """
    >>> _has_ajaxcrawlable_meta('<html><head><meta name="fragment"  content="!"/></head><body></body></html>')
    True
    >>> _has_ajaxcrawlable_meta("<html><head><meta name='fragment' content='!'></head></html>")
    True
    >>> _has_ajaxcrawlable_meta('<html><head><!--<meta name="fragment"  content="!"/>--></head><body></body></html>')
    False
    >>> _has_ajaxcrawlable_meta('<html></html>')
    False
    """

    # Stripping scripts and comments is slow (about 20x slower than
    # just checking if a string is in text); this is a quick fail-fast
    # path that should work for most pages.
    if 'fragment' not in text:
        return False
    if 'content' not in text:
        return False

    text = html.remove_tags_with_content(text, ('script', 'noscript'))
    text = html.replace_entities(text)
    text = html.remove_comments(text)
    return _ajax_crawlable_re.search(text) is not None
```
找到页面上名字为frgment，并且有content，然后调用3个方法去处理text,然后使用正则表达式去匹配他。
* remove_tags_with_content:这个方法就是从一个html文本中去除指定的标签及其内容
* replace_entities: 转化指定的html内容为unicode charactor
* remove_comments: 提取注释以外的内容。

