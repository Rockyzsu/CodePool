## Settings 设置

### 填充设置方法
* 命令行
* 每个爬虫设置
* 工程设置
* 默认设置
* 默认全局设置

#### 命令行方式

```cmd
scrapy crawl myspider -s LOG_FILE=scrapy.log
```

#### 每个爬虫的设置

```python
class MySpider(scrapy.Spider):
    name = 'myspider'

    custom_settings = {
        'SOME_SETTING': 'some value',
    }
```
#### 工程设置
```python
settings.py文件
```
#### 每个命令的默认设置
每个scrapy工具，都有自己的默认设置的

#### 默认全局设置
默认全局设置在scrapy.settings.default_settings

### 如何访问设置
```python

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://example.com']

    def parse(self, response):
        print("Existing settings: %s" % self.settings.attributes.keys())
```

```python
class MyExtension(object):
    def __init__(self, log_is_enabled=False):
        if log_is_enabled:
            print("log is enabled!")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.getbool('LOG_ENABLED'))
```

#### AWS_ACCESS_KEY_ID
aws相关参数

#### AWS_SECRET_ACCESS_KEY
aws相关参数

#### BOT_NAME
和工程名字相同（使用startproject创建）

#### CONCURRENT_ITEMS
item processor并发处理的最大item数

#### CONCURRENT_REQUESTS
下载器并发最大请求数

#### CONCURRENT_REQUESTS_PER_DOMAIN
单个域并发请求的最大值
#### CONCURRENT_REQUEST_PER_IP
并发请求每个ip的最大请求数

#### DEFAULT_ITEM_CLASS
scrapy shell的默认item类

#### DEFAULT_REQUEST_HEADERS
```json
{
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}
```
可以修改默认DefaultHeaderMiddleware

#### DEPTH_LIMIT
抓取深度，默认是 0表示不限制

#### DEPTH_PRIORITY
* 0 无优先级
* 正数 ： 深度大的后处理，宽度优先搜索
* 负数： 深度大的先处理，深度优先搜索

#### DEPTH_STATS
是否收集最大深度统计

#### DEPTH_STATS_VERBOSE
每个深度的统计信息

#### DNSCACHE_ENABLED
是否启用dns缓存

#### DNSCACHE_SIZE
缓存大小

#### DNS_TIMEOUT
处理dns超时的秒数，支持浮点

#### DOWNLOADER
抓取者使用的下载器

#### DOWNLOADER_HTTPCLIENTFACTORY
下载器使用的http 客户端工厂

#### DOWNLOADER_CLIENTCONTEXTFACTORY
上下文工厂，是否证书验证，认证等

#### DOWNLOADER_CLIENT_TLS_METHOD
下载器客户端的tls方法
#### DOWNLOADER_MIDDLEWARES
下载中间件
#### DOWNLOADER_MIDDLEWARES_BASE
```json
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
```
这些是下载中间件默认的，数值低的先调用，数值高的后调用，不建议调整这个参数， 建议调整DOWNLOADER_MIDDLEWARES。

#### DOWNLOADER_STATS
是否启用下载器统计信息收集

#### DOWNLOAD_DELAY
现在延迟设置， 防止对一个网址连续请求被封。

#### DOWNLOAD_HANDLERS
下载处理器

#### DOWNLOAD_HANGDLERS_BASE
```json
{
    'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
    'ftp': 'scrapy.core.downloader.handlers.ftp.FTPDownloadHandler',
}
```
默认下载处理器，
#### DOWNLOAD_TIMEOUT
下载在等待超时的秒数

#### DOWNLOAD_MAXSIZE
最大响应流的大小，0代表不限制响应流的大小

#### DOWNLOAD_WARNSIZE
响应流大小达到这个值，提示警告信息

#### DOWNLOAD_FAIL_ON_DATALOSS
是否失败在那些终端的响应上

#### DUPERFILTER_CLASS
这个类去出去重复的请求
#### DUPEFILTER_DEBUG
启用后，日志信息可以更丰富， 每个请求的url都会记录下来

#### EDITOR
vi on unix , EDLE on windows

#### EXTENSIONS
启用的扩展

#### EXTENSIONS_BASE
```json
{
    'scrapy.extensions.corestats.CoreStats': 0,
    'scrapy.extensions.telnet.TelnetConsole': 0,
    'scrapy.extensions.memusage.MemoryUsage': 0,
    'scrapy.extensions.memdebug.MemoryDebugger': 0,
    'scrapy.extensions.closespider.CloseSpider': 0,
    'scrapy.extensions.feedexport.FeedExporter': 0,
    'scrapy.extensions.logstats.LogStats': 0,
    'scrapy.extensions.spiderstate.SpiderState': 0,
    'scrapy.extensions.throttle.AutoThrottle': 0,
}
```
扩展基类，内建的一些扩展

#### FEED_TEMPDIR
这个目录，可以在保存文件到ftp或者amazon s3存储上的临时文件存放位置

#### FTP_PASSIVE_MODE
ftp使用被动模式 
 
#### FTP_PASSWORD
FTP请求的密码，
#### FTP_USER
FTP请求的用户名

#### ITEM_PIPELINES
设置item管道处理，数值越低的越先处理，数值越大后处理。可以把去重的，验证的放前面，最后放一个持久化的，当然也可以放多个持久化的，但是需要保证前面的持久化都有返回。

#### ITEM_PIPELINE_BASE
ITEM PIPELINE的基类， 不建议修改

#### LOG_ENABLED
是否启用日志记录
#### LOG_ENCODING
日志的编码

#### LOG_FILE
日志文件

#### LOG_FORMAT
默认是'%(asctim)s [%(name)s] %(levelname)s: %(message)s'

#### LOG_DATEFORMAT
日志的日期格式。 默认是'%Y-%m-%d %H:%M:%S'

#### LOG_LEVEL
默认是DEBUG

#### LOG_STDOUT
所有终端输出的信息都会写入到log信息中

#### LOG_SHORT_NAMES
如果为true,只显示/路径的

#### MEMDEBUG_ENABLED
是否启用内存调试功能

#### MEMDEBUG_NOTIFY
设置内存调试的邮箱

#### MEMUSAGE_ENABLED
是否启用内存使用扩展，

#### MEMUSAGE_LIMIT_MB
最大的内存使用

#### MEMUSAGE_CHECK_INTERVAL_SECONDS
内存监测的间隔，默认60s

#### MEMUSAGE_NOTIFY_MAIL 
通知的email列表

#### MEMUSAGE_WARNING_MB
内存使用的警告大小

#### NEWSPIDER_MODULE
新爬虫的模块


#### RANDOMIZE_DOWNLOAD_DELAY
随机下载延迟， 0.5 * download_delay and 1.5 * download_delay

#### REACTOR_THREADPOOL_MAXSIZE
twiisted 反应堆线程池的大小
#### REDIRECT_MAX_TIMES
请求被重定向的最大次数
#### REDICT_PRIORITY_ADJUST
正数代表优先级提高，
负数代表优先级降低
#### RETRY_PRIORITY_ADJUST
重试的优先级调整

#### ROBOTSTXT_OBEY
启用表示遵守robots.txt策略，这个值默认是false的， 但是通过startproject后默认为true的
#### SCHEDULER
调度器，就是抓取者的调度器

#### SCHEDULER_DEBUG
调度器调试

#### SCHEDULER_DISK_QUEUE
调度队列

#### SCHEDULER_MEMORY_QUEUE
内存调度队列

#### SCHEDULER_PRIORITY_QUEUE
调度的优先级队列

#### SPIDER_CONTRACTS
蜘蛛契约， 不知道是个啥东东

#### SPIDER_CONTRACTS_BASE
蜘蛛契约基类

#### SPIDER_LOADER_CLASS
蜘蛛加载器类
#### SPIDER_LOADER_WARN_ONLY
忽略爬虫加载器的警告

#### SPIDER_MIDDLEWARES
爬虫中间件
#### SPIDER_MIDDLERWARES_BASE
爬虫中间件基类

#### SPIDER_MODULES
scrapy查找爬虫的模块

#### STATS_CLASS
收集统计信息的类

#### STAT_DUMP
爬虫完成是否统计信息

#### STATSMAILER_RCPTS
发送统计信息，在爬虫完成抓取的时候

#### TELNETCONSOLE_ENABLED
是否启用telnet终端

#### TELNETCONSOLE_PORT
TELNET的端口

#### TEMPLATES_DIR
模板文件夹，

#### URLLENGTH_LIMIT
url长度限制，
#### USER_AGENT
默认用户代理


### 其他设置

[参考地址](https://doc.scrapy.org/en/latest/topics/settings.html)

