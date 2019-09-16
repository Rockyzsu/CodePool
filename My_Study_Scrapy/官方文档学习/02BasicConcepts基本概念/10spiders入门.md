# Spider介绍
## Spider简介
Spider是一个爬虫基类， 所有的爬虫类都直接或者间接继承这个类。
## scrapy.Spider学习
这个类是爬虫的基类，其他的爬虫都必须间接或者直接继承这个类，这个类基本不需要提供具体的方法实现。
下面对Spider主要的属性和方法介绍下，可能会带一些源码分析。
### name
这个就是设置爬虫名字的，这个值必须是工程级别唯一的，这个字段也是必须设置的。在Python2中，name必须是ascii值。
### name 源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    name = None
    custom_settings = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
```
我们可以看到初始化方法，设置name属性，然后判断属性是否是None，如果是那就抛出一个异常。
### allowed_domain 
这个是可选的， 如果设置了，请求的url必须是这个域内的地址，超出这个域的过滤掉。
### allowed_domain源码分析

### start_urls
这个不是必须的，但是我们写爬虫就是要爬取数据，不写启动的url，那不搞笑吗，这个就是设置我们爬虫启动的url列表，list类型。
### start_urls源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
```
我们可以看出来，如果我们没有设置start_urls，默认值会是[]，这个属性和start_request方法一起配合的。
### custom_settings
这个是自定义设置的， 我们有默认的工程设置， 但是工程内有多个爬虫， 我们想给部分爬虫设置单独的设置，就需要这个属性的设置了。
### custome_settings源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {}, priority='spider')
```
在scrapy.crawler.py文件中有如下代码：
```python
     def __init__(self, spidercls, settings=None):
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self.spidercls = spidercls
        self.settings = settings.copy()
        self.spidercls.update_settings(self.settings)

        d = dict(overridden_settings(self.settings))
        logger.info("Overridden settings: %(settings)r", {'settings': d})

        self.signals = SignalManager(self)
        self.stats = load_object(self.settings['STATS_CLASS'])(self)

        handler = LogCounterHandler(self, level=self.settings.get('LOG_LEVEL'))
        logging.root.addHandler(handler)
        if get_scrapy_root_handler() is not None:
            # scrapy root handler already installed: update it with new settings
            install_scrapy_root_handler(self.settings)
        # lambda is assigned to Crawler attribute because this way it is not
        # garbage collected after leaving __init__ scope
        self.__remove_handler = lambda: logging.root.removeHandler(handler)
        self.signals.connect(self.__remove_handler, signals.engine_stopped)

        lf_cls = load_object(self.settings['LOG_FORMATTER'])
        self.logformatter = lf_cls.from_crawler(self)
        self.extensions = ExtensionManager.from_crawler(self)

        self.settings.freeze()
        self.crawling = False
        self.spider = None
        self.engine = None
```
我们看到第一段代码，是更新设置的，我们的custome_settings是爬虫级别的，默认的settings.py文件的优先级是工程级别的，这个爬虫级别的优先级比工程级别的优先级高， 会使用custom_settings的设置覆盖工程级别的设置。
第二段代码是调用第一段代码的方法的，我们的爬虫类是被爬虫者调用的。
### crawler
该属性由初始化类之后由from_crawler（）类方法设置，并链接到此蜘蛛实例绑定到的Crawler对象。
Crawlers在项目中封装了大量组件，用于单一访问（例如扩展，中间件，信号管理器等）。
### crawler源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider
    def _set_crawler(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        crawler.signals.connect(self.close, signals.spider_closed)
```
我们可以看出来，crawler对象通过from_crawler方法传递过来，最终将cralwer设置到self的crawler属性上。并且给爬取者的关闭绑定了爬虫关闭的回调方法。

### settings
获取爬虫的设置信息
### settings源码分析
这个在scrawler源码分析中，setting的设置是从crawler.settings获取到的。
### logger
根据爬虫名字创建的一个log对象。
### logger源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    @property
    def logger(self):
        logger = logging.getLogger(self.name)
        return logging.LoggerAdapter(logger, {'spider': self})

```
这个日志是根据爬虫的名字来设置的， 所以再次强调了官方文档说的爬虫名字不能重名，必须工程级别唯一的。

### from_crawler(crawler, *args, **kwargs)
这是一个类方法，去创建你的爬虫。
### from_crawler(crawler, *args, **kwargs)源码分析
这个上面的crawler源码分析已经提到了。
### start_requests()
默认实现是遍历start_urls的url，执行Request(url, dont_filter=True)，我们可以不指定start_urls，在这里设置我们的url列表并遍历url列表。
### start_requests()源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
 def start_requests(self):
        cls = self.__class__
        if method_is_overridden(cls, Spider, 'make_requests_from_url'):
            warnings.warn(
                "Spider.make_requests_from_url method is deprecated; it "
                "won't be called in future Scrapy releases. Please "
                "override Spider.start_requests method instead (see %s.%s)." % (
                    cls.__module__, cls.__name__
                ),
            )
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)

    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        return Request(url, dont_filter=True)
```
这个方法看着代码挺多的，其实没啥， 先判断下`make_requests_from_url`是不是被重写了。如果是就遍历urls,每个都执行`make_requests_from_url`,如果没有被重写，就使用Resquest去请求。 官方文档已经没有make_request_from_url这个方法了，这个方法的注释也表明这个方法已经不用了，但是为了兼容，这个保留了。貌似scrapy-json 里面还用到了`make_requests_from_url`这个方法。
### parse(response)
这是默认的下载响应流的回调方法
返回值只能是Request,dict,Item对象。
### parse(response)源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
```
我们可以看到这个parse方法是个空的，子类继承必须要实现这个方法，不实现就会抛出异常。
### log(message[, level, component])
这个就是写日志的。
### log(message[, level, component])源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    def log(self, message, level=logging.DEBUG, **kw):
        """Log the given message at the given log level

        This helper wraps a log call to the logger within the spider, but you
        can use it directly (e.g. Spider.logger.info('msg')) or use any other
        Python logger too.
        """
        self.logger.log(level, message, **kw)
```
这个就是将self.logger.log方法快照给了self,我们可以直接使用self.log，内部还是调用的self.logger.log。并且这个方法也提供了level的默认值。
### closed(reason)
关闭爬虫，发送关闭信号。
### closed(reason)源码分析
在`scrapy.spiders.__init__.py`文件中有如下代码：
```python
    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)
```
先获取closed方法，如果有且可调用的话，就执行close方法。
## 使用样例
```python
import scrapy


class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
```
这是最简单的样例了。
```python
import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    def start_requests(self):
        yield scrapy.Request('http://www.example.com/1.html', self.parse)
        yield scrapy.Request('http://www.example.com/2.html', self.parse)
        yield scrapy.Request('http://www.example.com/3.html', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```
不使用start_urls属性，我们自己重写start_request方法，自己去遍历urls列表。
## 爬虫参数
设置爬虫参数，我们只需要-a选项即可。
使用如下
```cmd
scrapy crawl myspider -a category=electronics
```
然后在我们的爬虫的__init__方法中即可使用
```python
import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]
        # ...
```
我们使用命令行传递过来的参数，默认会直接设置self.category=category ,我们不需要再设置的。这个在我们的start_urls不确定，需要传递的参数才能确认的时候才用的。

