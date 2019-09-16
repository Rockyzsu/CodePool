## Signals

信号使用样例
```python
from scrapy import signals
from scrapy import Spider


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DmozSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)


    def parse(self, response):
        pass
```
### 内置信号参考

#### scrapy.signals.engine_started()
爬虫引擎启动的时候
#### scrapy.signals.engine_stopped()
引擎关闭的时候
#### scrapy.signals.item_scraped(item, response, spider)
item被抓取，不能过去通过了itempipeline的时候触发
#### scrapy.signals.item_dropped(item, response, exception, spider)
item被itempipeline丢弃的时候触发
#### scrapy.signals.spider_closed(spider, reason)
爬虫关闭的时候触发
reason 有finished,cancelled,shutdown三个值
#### scrapy.signals.spider_opened(spider)
爬虫打开的时候触发
#### scrapy.signals.spider_idle(spider)
爬虫空闲的时候触发
* 请求等待去下载
* 请求调度
* item被处理在pipeline
在爬虫完成关闭的时候，spider_closed信号被发送
你可以raise DontCloseSpider异常去阻止爬虫的关闭
#### scrapy.signals.spider_error(failure, response, spider)
爬虫回调生成错误的时候
#### scrapy.signals.request_scheduled(request, spider)
引擎调度这个请求
#### scrapy.signals.request_dropped(request, spider)
请求被拒绝的时候
#### scrapy.signals.response_received(response, request, spider)
引擎接受到新的响应从下载器
#### scrapy.signals.response_downloaded(response, request, spider)
响应下载完毕的时候
