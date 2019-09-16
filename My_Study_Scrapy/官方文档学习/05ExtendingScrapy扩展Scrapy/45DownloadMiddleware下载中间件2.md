## DownloadMiddleware下载中间件

### 内置的下载中间件参考

#### CookiesMiddleware
##### class scrapy.downloadermiddlewares.cookies.CookiesMiddleware
此中间件允许处理需要cookie的站点，例如使用会话的站点。它跟踪Web服务器发送的cookie，然后像Web浏览器那样在后续请求（从那个蜘蛛）发送回它们。

可用的设置
* COOKIES_ENABLED :默认True,如果禁用，就不会给服务器发送cookie信息
* COOKIES_DEBUG：默认false,如果启用，scrapy会记录所有cookies信息发送。

##### 一个爬虫多个cookie会话
这是支持一个爬虫多个cookie会话的，使用cookiejar在request的meta中，默认使用的单个cookie jar，你可以指定启用cooked会话

```python
for i, url in enumerate(urls):
    yield scrapy.Request(url, meta={'cookiejar': i},
        callback=self.parse_page)
```

这样使用cookiejar不是粘性的， 你如果在parse方法使用Request方法，必须继续指定cookiejar
```python
def parse_page(self, response):
    # do some processing
    return scrapy.Request("http://www.example.com/otherpage",
        meta={'cookiejar': response.meta['cookiejar']},
        callback=self.parse_other_page)
```

启用COOKIES_DEBUG会得到如下信息

```cmd
2011-04-06 14:35:10-0300 [scrapy.core.engine] INFO: Spider opened
2011-04-06 14:35:10-0300 [scrapy.downloadermiddlewares.cookies] DEBUG: Sending cookies to: <GET http://www.diningcity.com/netherlands/index.html>
        Cookie: clientlanguage_nl=en_EN
2011-04-06 14:35:14-0300 [scrapy.downloadermiddlewares.cookies] DEBUG: Received cookies from: <200 http://www.diningcity.com/netherlands/index.html>
        Set-Cookie: JSESSIONID=B~FA4DC0C496C8762AE4F1A620EAB34F38; Path=/
        Set-Cookie: ip_isocode=US
        Set-Cookie: clientlanguage_nl=en_EN; Expires=Thu, 07-Apr-2011 21:21:34 GMT; Path=/
2011-04-06 14:49:50-0300 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://www.diningcity.com/netherlands/index.html> (referer: None)
[...]
```

#### DefaultHeadersMiddleware

##### class scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware
可以通过设置DEFAULT_REQUEST_HEADERS设置默认请求头

#### DownloadTimeoutMiddleware

##### class scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware
设置下载超时的DOWNLOAD_TIMEOUT

#### HttpAuthMiddleware
##### class scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware
这个中间件提供认证
设置http_user,http_pass即可
```python
from scrapy.spiders import CrawlSpider

class SomeIntranetSiteSpider(CrawlSpider):

    http_user = 'someuser'
    http_pass = 'somepass'
    name = 'intranet.example.com'

    # .. rest of the spider code omitted ...
```
#### HttpCacheMiddleware 
##### class scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware
这个中间件提供低级别的http 请求和响应缓存。
* HTTPCACHE_POLICY:缓存策略
* HTTPCACHE_STORAGE:缓存的存储
* HTTPCACHE_ENABLED: 缓存启用
* HTTPCACHE_EXPIRATION_SECS:缓存过期秒
* HTTPCACHE_DIR:缓存的dir
* HTTPCACHE_IGNORE_HTTP_CODE:不缓存再有指定代码的响应
* HTTPCACHE_IGNORE_SCHEMES:不缓存指定url架构的响应，默认是['file']
* HTTPCACHE_DBM_MODULE: 这个设置知道哪个DBM的模块
* HTTPCACHE_GZIP: 默认False,压缩缓存数据
* HTTPCACHE_ALWAYS_STORE: 如果启用， 将缓存所有响应
* HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS: 缓存控制指令列表中被忽略的响应。
如果不启用缓存可以使用dont_cache=False在metakey中的


#### HttpCompressionMiddleware
##### class scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware
这个中间件是允许压缩的
* COMPRESSION_ENABLED : 默认是启用的

#### HttpProxyMiddleware
##### class scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware
代理中间件
* http_proxy
* https_proxy
* no_proxy
* HTTP_PROXY_ENABLED: 是否启用代理中间件
* HTTPPROXY_AUTH_ENCODING: 默认编码

捏可以通过meta key 设置每一个请求的代理，proxy=http://some_proxy_server:port或者http://username:password@some_proxy_server:port，这样会忽略环境变量的设置。


#### RedirectMiddleware
##### class scrapy.downloadermiddlewares.redirect.RedirectMiddleware
这个中间件提供重定向
* REDIRECT_ENABLED: 启用重定向
* REDIRECT_MAX_TIMES: 最大重定向的次数
如果Request.meta有dont_redirect 设置True,就会忽略这个中间件

如果你想重定向中间件护绿301，302响应码
```python
class MySpider(CrawlSpider):
    handle_httpstatus_list = [301, 302]
```


#### MetaRefreshMiddleware
##### class scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware
该中间件处理基于元刷新html标签的请求重定向。
* METAREFERSH_ENABLED: 默认True,是否启用
* METAREFERSH_MAXDELAY: 遵循重定向的最大元刷新延迟（以秒为单位）。 某些站点使用元刷新重定向到会话过期页面，所以我们将自动重定向制为最大延迟。

#### RetryMiddleware
##### class scrapy.downloadermiddlewares.retry.RetryMiddleware
重试中间件
* RETRY_ENABLED: 启用不启用
* RETRY_TIMES:重用次数
* RETRY_HTTP_CODE: 默认是 [500,502,503,504,408]


#### RobotsTxtMiddleware
##### class scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware
这个中间件过滤掉robots.txt排除标准禁止的请求。
* ROBOTSTXT_OBEY: 是否遵守REBOT


#### DownloaderStats
##### class scrapy.downloadermiddlewares.stats.DownloaderStats
存储下载和响应和异常等信息
* DOWNLOADER_STATS: 是否启用下载状态

#### UserAgentMiddleware
##### class scrapy.downloadermiddlewares.useragent.UserAgentMiddleware
这个中间件提供重写默认用户代理的
* USER_AGENT

#### AjaxCrawlMiddleware
##### class scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware
根据meta-fragment html标签查找“AJAX可抓取”页面变体的中间件。
* AJAXCRAWL_ENABLED : 是否启用AJAXCRAWL

