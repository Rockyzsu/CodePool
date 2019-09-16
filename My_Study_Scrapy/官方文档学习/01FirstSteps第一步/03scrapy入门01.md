# scrapy入门
## 任务描述
1.  创建爬虫工程
2.  编写爬虫去抓取站点和提取数据
3.  通过命令行导出数据
4.  改变爬虫去追踪链接
5.  使用爬虫参数

## 创建爬虫工程
``` python
scrapy startproject tutorial
```
## 源码分析工程创建过程
我们可以从`scrapy.commands.startproject.py`这个文件看到如下部分代码。
``` python
        self._copytree(self.templates_dir, abspath(project_dir))
        move(join(project_dir, 'module'), join(project_dir, project_name))
        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_dir,
                string.Template(path).substitute(project_name=project_name))
            render_templatefile(tplfile, project_name=project_name,
                ProjectName=string_camelcase(project_name))
        print("New Scrapy project %r, using template directory %r, created in:" % \
              (project_name, self.templates_dir))
        print("    %s\n" % abspath(project_dir))
        print("You can start your first spider with:")
        print("    cd %s" % project_dir)
        print("    scrapy genspider example example.com")
```
简单看看吧， 它调用了copytree方法把一个文件夹的内容（其实是scrapy的模板文件夹`scrapy.templates`）复制到我们的工程文件夹，调用move完成目录名字的重命名工作，先后使用string.Template(path).substitute完成目录下文件内部内容的替换工作。最后使用print打印一些语句。这也是我们创建工程看到的内容。
如果有兴趣可以自己比较下我们创建的工程下的文件和模板文件夹下的内容，你能更清楚这个startproject内部做了啥工作。

## 编写爬虫
添加quotes_spider.py在tutorial.spiders目录下，内容如下
``` python
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```
name:设置爬虫的名字，工程级别是唯一的
start_requests:必须返回一个迭代的Request
parse:默认的处理响应方法
##　源码分析这几个爬虫参数

`scrapy.spiders.__init__.py` 文件里面定义了scrapy.Spider类

**name代码段**
``` python
name=None
```

**parse代码段**
``` python
def parse(self, response):
    raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
```
我们可以看到模式方法parse，如果子类不实现实惠抛出异常的。你如果想知道为何这个爬虫调用默认的parse解析的话可以从`scrapy.core.scraper.py`文件看到这段代码:
``` python
    def call_spider(self, result, request, spider):
        result.request = request
        dfd = defer_result(result)
        dfd.addCallbacks(request.callback or spider.parse, request.errback)
        return dfd.addCallback(iterate_spider_output)
```
这个call_spider具体代码不详细讲， 我们只看 `dfd.addCallbacks(request.callback or spider.parse, request.errback)`就够了，先使用你请求的默认回调方法，如果没有就使用parse方法。

**start_requests代码段**
``` python
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
我们可以看到，我们看到start_requests这个方法调用了make_request_from_url这个方法，但是make_request_from_url这个方法提示不推荐使用了,建议直接使用Request方法，回到start_requests方法，我们看到首先判断make_requests_from_url方法是否被子类重写了，如果被重写了。就提示一个警告信息。然后遍历start_urls列表调用make_request_from_url()完成请求调用。否则就使用Request方法

## 运行爬虫
打开命令行，进入工程目录执行如下命令
```cmd
scrapy crawl quotes
```
运行完命令，我们发现我们已经抓取2个页面到我们的工程目录下了。当然我们也看到很多的输出，我们整理下整个爬虫的工作步骤。

* 启动爬虫引擎
* 加载设置文件
* 启用扩展
* 启用下载中间件
* 启用爬虫中间件
* 启动pipeline
* 爬虫启动，开始工作
* 爬虫结束， 引擎收集统计信息，清理工作
### 输出信息代码分析
先看下输出信息
``` cmd
e:\ZhaojiediProject\github\My_Study_Scrapy\官方文档学习\demo\tutorial>scrapy crawl quotes
2017-10-17 15:20:48 [scrapy.utils.log] INFO: Scrapy 1.3.3 started (bot: tutorial)
2017-10-17 15:20:48 [scrapy.utils.log] INFO: Overridden settings: {'BOT_NAME': 'tutorial', 'NEWSPIDER_MODULE': 'tutorial.spiders', 'ROBOTSTXT_OBEY': True, 'SPIDER_MODULES': ['tutorial.spiders']}
2017-10-17 15:20:48 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.logstats.LogStats']
2017-10-17 15:20:51 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2017-10-17 15:20:51 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2017-10-17 15:20:51 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2017-10-17 15:20:51 [scrapy.core.engine] INFO: Spider opened
2017-10-17 15:20:51 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2017-10-17 15:20:51 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2017-10-17 15:20:51 [scrapy.core.engine] DEBUG: Crawled (404) <GET http://quotes.toscrape.com/robots.txt> (referer: None)
2017-10-17 15:20:52 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
2017-10-17 15:20:52 [quotes] DEBUG: Saved file quotes-1.html
2017-10-17 15:20:53 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/2/> (referer: None)
2017-10-17 15:20:53 [quotes] DEBUG: Saved file quotes-2.html
2017-10-17 15:20:53 [scrapy.core.engine] INFO: Closing spider (finished)
2017-10-17 15:20:53 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 675,
 'downloader/request_count': 3,
 'downloader/request_method_count/GET': 3,
 'downloader/response_bytes': 5976,
 'downloader/response_count': 3,
 'downloader/response_status_count/200': 2,
 'downloader/response_status_count/404': 1,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2017, 10, 17, 7, 20, 53, 532967),
 'log_count/DEBUG': 6,
 'log_count/INFO': 7,
 'response_received_count': 3,
 'scheduler/dequeued': 2,
 'scheduler/dequeued/memory': 2,
 'scheduler/enqueued': 2,
 'scheduler/enqueued/memory': 2,
 'start_time': datetime.datetime(2017, 10, 17, 7, 20, 51, 402278)}
2017-10-17 15:20:53 [scrapy.core.engine] INFO: Spider closed (finished)
```
---
我们可以找到在scrapy.crawler.py文件的类CrawlerProcess初始化方法调用了log_scrapy_info方法
``` python
def log_scrapy_info(settings):
    logger.info("Scrapy %(version)s started (bot: %(bot)s)",
                {'version': scrapy.__version__, 'bot': settings['BOT_NAME']})
    logger.info("Versions: %(versions)s",
                {'versions': ", ".join("%s %s" % (name, version)
                    for name, version in scrapy_components_versions()
                    if name != "Scrapy")})
```
这个日志打印了scrapy启动的版本和机器人名字信息
---
我们找到在scrapy.crawler.py文件的类Crawler初始化方法调用方法
``` python
       d = dict(overridden_settings(self.settings))
        logger.info("Overridden settings: %(settings)r", {'settings': d})
```
这个日志打印了重写的设置
---
我们在scrapy.middleware.py的MiddlewareManager类from_settings方法中找到如下代码
``` python
        logger.info("Enabled %(componentname)ss:\n%(enabledlist)s",
                    {'componentname': cls.component_name,
                     'enabledlist': pprint.pformat(enabled)},
                    extra={'crawler': crawler})
```
这个日志打印了启动的中间件名字机器列表信息

我们在scrapy.core.engine.py的ExecutionEngine类oen_spider方法找到如下代码
``` python
  logger.info("Spider opened", extra={'spider': spider})
```
我们在scrapy.extensions.logstats.py的logStats类log方法中找到如下代码
``` python
    def log(self, spider):
        items = self.stats.get_value('item_scraped_count', 0)
        pages = self.stats.get_value('response_received_count', 0)
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier
        self.pagesprev, self.itemsprev = pages, items

        msg = ("Crawled %(pages)d pages (at %(pagerate)d pages/min), "
               "scraped %(items)d items (at %(itemrate)d items/min)")
        log_args = {'pages': pages, 'pagerate': prate,
                    'items': items, 'itemrate': irate}
        logger.info(msg, log_args, extra={'spider': spider})
``` 
从stats对象中获取抓取到的信息，并报告信息

我们在scrapy.extensions.telnet.py的TelnetConsole类start_listening方法中找到如下代码
``` python
    def start_listening(self):
        self.port = listen_tcp(self.portrange, self.host, self)
        h = self.port.getHost()
        logger.debug("Telnet console listening on %(host)s:%(port)d",
                     {'host': h.host, 'port': h.port},
                     extra={'crawler': self.crawler})
``` 
这个日志打印了telnet终端信息
我们在scrapy.core.engine.py的ExecutionEngine类_download方法中找到如下代码
``` python
   def _on_success(response):
            assert isinstance(response, (Response, Request))
            if isinstance(response, Response):
                response.request = request # tie request to response received
                logkws = self.logformatter.crawled(request, response, spider)
                logger.log(*logformatter_adapter(logkws), extra={'spider': spider})
                self.signals.send_catch_log(signal=signals.response_received, \
                    response=response, request=request, spider=spider)
            return response
``` 

我们在scrapy.statscollectors.py的StatsCollector类close_spider方法中找到如下代码
``` python
    def close_spider(self, spider, reason):
        if self._dump:
            logger.info("Dumping Scrapy stats:\n" + pprint.pformat(self._stats),
                        extra={'spider': spider})
        self._persist_stats(self._stats, spider)
```
这个日志打印了scrapy整体的统计信息