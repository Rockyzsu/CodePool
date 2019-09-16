##CrawlSpider简介
CrawlSpider是抓取有规律的网址使用最广的爬虫类。它提供一些规则集，匹配指定的规则，对应指定的parse回调方法。
### rules
这是一个rule对象的集合，每个rule对象定义了网址对应的解析类。
### parse_start_url(response)
这个方法是请求流的回调方法，返回值只能是Item,Request,Dict。
### parse_start_url(response):源码分析
在`scrapy.spiders.crawl.py`文件中，有如下代码：
```python
    def parse(self, response):
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)
    def parse_start_url(self, response):
        return []
    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item

        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item

```
这个爬虫类CrawlSpider是继承基础爬虫类的，所以必须实现parse方法的。
##抓取规则（Crawling rules)
`class scrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)`
* link_extractor是一个LinkExtractor对象，
* callback指定回调方法。
* cb_kwargs: 传递给回调方法的关键参数
* follow: 布尔值，提取链接
* process_links： 是一个回调方法，这个多用于过滤
* process_request: 是一个回调或者string，必须返回一个request或者None
##抓取规则（Crawling rules)源码分析
在`scrapy.spiders.crawl.py`文件中，有如下代码：
```python
def identity(x):
    return x
class Rule(object):
    def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=identity):
        self.link_extractor = link_extractor
        self.callback = callback
        self.cb_kwargs = cb_kwargs or {}
        self.process_links = process_links
        self.process_request = process_request
        if follow is None:
            self.follow = False if callback else True
        else:
            self.follow = follow
```
上面已经介绍了。各个属性的含义了。 
## 样例
```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #提取链接要匹配category.php，但是不匹配subsection.php
        #并且追踪链接，么有callback的设置，意味着follow=True
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
        # 提取链接匹配item.php的，使用parse_item去解析响应流
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
```