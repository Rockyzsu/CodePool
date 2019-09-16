## Extension扩展

### class scrapy.extensions.logstats.LogStats
抓取页面数量和抓取到的items基本统计

### class scrapy.extensions.corestats.CoreStats
核心统计启用，就一类统计就启用了

### class scrapy.extensions.telnet.TelnetConsole
提供一个telnet终端进入python解释器， 是一个非常有用的调试手段

需要设置TELNETCONSOLE_ENABLED,监听在TELNETCONSOLE_PORT上。 

### class scrapy.extensions.memusage.MemoryUsage

这个扩展在window上是部工作的。
检测内存，发送通知email在超出一个阈值,MEMUSAGE_WARNING_MB
关闭爬虫在超出一个阈值,MEMUSAGE_LIMIT_MB
相关的设置

* MEMUSAGE_ENABLED: 是否启用
* MEMUSAGE_LIMIT_MB:最大使用内存
* MEMUSAGE_WARNING_MB:警告内存
* MEMUSAGE_NOTIFY_MAIL:通知email
* MEMUSAGE_CHECK_INTERVAL_SECONDS:检查间隔

### class scrapy.extensions.memdebug.MemoryDebugger 
内存调试扩展，需要设置MEMDEBUG_ENABLED开启，统计信息就存储stats中

### class scrapy.extensions.closespider.CloseSpider
关闭爬虫在一定的条件触发

CLOSESPIDER_TIEMOUT:指定时间，爬虫打开时间超过这个值就关闭
CLOSESPIDER_ITEMCOUNT:达到指定item关闭，但是请求还是会继续一部分， 不超过并发量的。
CLOSESPIDER_PAGECOUNT:达到指定的页面个数
CLOSESPIDER_ERRORCOUNT:指定的错误个数

### class scrapy.extensions.statsmailer.StatsMailer

这个是一个简单的扩展去发送邮件在抓取结束的时候，STATSMAILER_RCPTS设置接收者

### class scrapy.extensions.debug.StackTraceDump
在收到SIGQUIT,SIGUSR2信号时候，转储下列信息
* 引擎状态 ： scrapy.utils.engine.get_engine_status()
* 现场参考
* 线程堆栈




