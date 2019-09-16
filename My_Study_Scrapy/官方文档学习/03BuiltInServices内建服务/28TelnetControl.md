## Telnet Control

### 访问telnet control

windows下可能没有telnet命令，可以访问[https://jingyan.baidu.com/article/1e5468f9033a71484961b7d7.html](https://jingyan.baidu.com/article/1e5468f9033a71484961b7d7.html)启用telnet功能。
```cmd
telnet localhost 6023
```

### telnet可用的变量
* crawler : scrapy.crawler.Crawler
* engine : Crawler.engine
* spider : 当前的激活的爬虫
* slot : 引擎槽
* extensions : Craler.extensions
* stats: Crawler.stats
* settings: Crawler.settings
* est : 打印引擎的状态
* prefs : 内存调试
* p : pprint.pprint
* hpy: 内存调试

### Telnet control 使用样例

```cmd 
telnet localhost 6023
>>> est()
Execution engine status

time()-engine.start_time                        : 8.62972998619
engine.has_capacity()                           : False
len(engine.downloader.active)                   : 16
engine.scraper.is_idle()                        : False
engine.spider.name                              : followall
engine.spider_is_idle(engine.spider)            : False
engine.slot.closing                             : False
len(engine.slot.inprogress)                     : 16
len(engine.slot.scheduler.dqs or [])            : 0
len(engine.slot.scheduler.mqs)                  : 92
len(engine.scraper.slot.queue)                  : 0
len(engine.scraper.slot.active)                 : 0
engine.scraper.slot.active_size                 : 0
engine.scraper.slot.itemproc_size               : 0
engine.scraper.slot.needs_backout()             : False

>>> engine.pause()

>>> engine.unpause()

>>> engine.stop()
Connection closed by foreign host.
```

### Telnet Control相关的设置

* TELNETCONSOLE_PORT ： 监听端口，默认是[6023,6073]
* TELNETCONSOLE_HOST : 监听的ip,默认是localhost.