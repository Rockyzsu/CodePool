## Benchmarking 

这个是scrapy抓取本地文件的样例，用于测试本地硬件环境下的抓取速度。

运行如下即可。
```cmd
scrapy bench
```
就可以得到如下信息
```cmd
2017-12-01 18:21:29 [scrapy.utils.log] INFO: Scrapy 1.4.0 started (bot: scrapybot)
2017-12-01 18:21:29 [scrapy.utils.log] INFO: Overridden settings: {'CLOSESPIDER_TIMEOUT': 10, 'LOGSTATS_INTERVAL': 1, 'LOG_LEVEL': 'INFO'}
2017-12-01 18:21:29 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.closespider.CloseSpider',
 'scrapy.extensions.logstats.LogStats']
2017-12-01 18:21:30 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2017-12-01 18:21:30 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2017-12-01 18:21:30 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2017-12-01 18:21:30 [scrapy.core.engine] INFO: Spider opened
2017-12-01 18:21:30 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:31 [scrapy.extensions.logstats] INFO: Crawled 77 pages (at 4620 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:32 [scrapy.extensions.logstats] INFO: Crawled 149 pages (at 4320 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:33 [scrapy.extensions.logstats] INFO: Crawled 213 pages (at 3840 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:34 [scrapy.extensions.logstats] INFO: Crawled 277 pages (at 3840 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:35 [scrapy.extensions.logstats] INFO: Crawled 333 pages (at 3360 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:36 [scrapy.extensions.logstats] INFO: Crawled 389 pages (at 3360 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:37 [scrapy.extensions.logstats] INFO: Crawled 445 pages (at 3360 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:38 [scrapy.extensions.logstats] INFO: Crawled 493 pages (at 2880 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:39 [scrapy.extensions.logstats] INFO: Crawled 541 pages (at 2880 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:40 [scrapy.core.engine] INFO: Closing spider (closespider_timeout)
2017-12-01 18:21:40 [scrapy.extensions.logstats] INFO: Crawled 589 pages (at 2880 pages/min), scraped 0 items (at 0 items/min)
2017-12-01 18:21:40 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 271341,
 'downloader/request_count': 605,
 'downloader/request_method_count/GET': 605,
 'downloader/response_bytes': 1881203,
 'downloader/response_count': 605,
 'downloader/response_status_count/200': 605,
 'finish_reason': 'closespider_timeout',
 'finish_time': datetime.datetime(2017, 12, 1, 10, 21, 40, 975675),
 'log_count/INFO': 17,
 'request_depth_max': 21,
 'response_received_count': 605,
 'scheduler/dequeued': 605,
 'scheduler/dequeued/memory': 605,
 'scheduler/enqueued': 12100,
 'scheduler/enqueued/memory': 12100,
 'start_time': datetime.datetime(2017, 12, 1, 10, 21, 30, 259147)}
2017-12-01 18:21:40 [scrapy.core.engine] INFO: Spider closed (closespider_timeout)
```


从上面的信息可以看出来， 抓取速度基本上能达到3000页面每分钟。 
