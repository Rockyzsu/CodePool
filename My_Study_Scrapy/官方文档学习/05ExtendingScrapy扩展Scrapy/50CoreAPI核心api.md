## CoreAPI核心api

这个文档主要面向开发扩展和中间件的

### Crawler Api
Scrapy api的主要入口点就是通过from_crawler类方法传递给扩展的crawler对象， 这个对象提供了对scrapy的核心组件的访问，这是扩展访问scrapy的唯一方式。也是调用他们的功能进入scrapy的唯一方式。

#### class scrapy.crawler.Crawler(spidercls, settings)
接受一个爬虫类，和一个setting

##### settings 
crawler的设置信息
##### signals
crawler的信号，这个是非常有用的
##### stats
crawler的统计信息
##### extensions
扩展管理器追踪和启用的扩展
##### engine
执行引擎，负责写到核心抓取逻辑，写帖调度器，下载器和爬虫

##### spider
crawler当前执行的爬虫，在crawl方法中创建spider

##### crawl(*argx,**kwargs)
通过使用给定的args,kwargs参数实例化其spider，启动爬虫程序


### class scrapy.crawler.CrawlerRunner(settings=None)
这是一个方便的帮助类，可以跟踪，管理和运行已经设置好的Twisted反应堆内的抓取程序。
#### crawl(crawler_or_spidercls, *args, **kwargs)
* crawler_or_spidercls: Crawler实例，Spider子类或者string
* args :初始化spider的参数
* kwargs ： 初始化spider的参数
#### Crawlers
通过crawl方法启用的一系列crawlers

#### create_crawler(crawler_or_spidercls)
创建一个crawler对象

#### join ()
返回一个延迟对象， 在所有管理的crawlers完成工作的时候触发。 

#### stop()
停止crawler的抓取工作。


### class scrapy.crawler.CrawlerProcess(settings=None)
这是一个在一个进程中运行多个爬虫Crawlers的类

这个类方法和CrawlerRunner差不过
#### start(stop_after_crawl=True)


### Settings Api
#### scrapy.settings.SETTINGS_PRIORITIES
这个定义各个设置的优先级的。 
```json
SETTINGS_PRIORITIES = {
    'default': 0,
    'command': 10,
    'project': 20,
    'spider': 30,
    'cmdline': 40,
}
```
#### scrapy.settings.get_settings_priority(priority)
查找给定的str的优先级
```cmd
In [3]: from scrapy.settings import get_settings_priority

In [4]: get_settings_priority('default')
Out[4]: 0

In [5]: get_settings_priority('cmdline')
Out[5]: 40
```
#### class scrapy.settings.Settings(values=None, priority='project')
这个对象存储scrapy的设置信息， 为了配置内部组件，也可以使用去跟深入的自定义。 

#### class scrapy.settings.BaseSettings(values=None, priority='project')
这个类实例像一个字典，但是存储(key,value)对并且可以冻结
##### copy()
对当前的settings做的深copy

##### copy_to_dict()
copy当前设置，并转化为dict,这个是非常有用的在shell中打印设置的。

##### freeze()
禁止对当前的设置进行改变
##### frozencopy()
返回一个直接copy
##### get(name, default=None)
获取指定的设置
##### getbool(name, default=False)
##### getdict(name, default=None)
##### getfloat(name, default=0.0)
##### getlist(name, default=None)
##### getpriority(name)
##### getwithbase(name)
##### maxpriority()
##### set(name, value, priority='project')
##### setmodule(module, priority='project')
##### update(values, priority='project')

### SpiderLoader API 
#### class scrapy.loader.SpiderLoader
##### from_settings(settings)
这个方法创建一个类实例，根据当前的工程设置。 加载爬虫是根据SPIDER_MODULES这个设置， 也就是settings.py文件的前面几行

##### load(spider_name)
获取爬虫类根据给定的名字。如果没有就触发一个KeyError
##### list()
获取工程的可用列表

##### find_by_request(request)
列出可以处理给定请求的蜘蛛名字，将尝试匹配请求的网址与蜘蛛的域名

### Signals API
#### class scrapy.signalmanager.SignalManager(sender=_Anonymous)
##### connect(receiver, signal, **kwargs)
连接一个信号到一个回调方法上
##### disconnect(receiver, signal, **kwargs)
断开一个连接
##### disconnect_all(signal, **kwargs)
断开所有信号连接
##### send_catch_log(signal, **kwargs)
发送信号，捕捉异常和记录他们
##### send_catch_log_deferred(signal, **kwargs)
和send_catch_log一样，不过支持下哦从信号处理那里返回deferreds

### Stats Collector API
#### class scrapy.statscollectors.StatsCollector
##### get_value(key, default=None)
#####  get_stats()
##### set_value(key, value)
##### set_stats(stats)
设置统计
##### inc_value(key, count=1, start=0)
增加值
##### max_value(key, value)
##### min_value(key, value)
##### clear_stats()
清空统计
##### open_spider(spider)
打开给定爬虫的统计信息收集
##### close_spider(spider)
关闭给定爬虫，调用后， 不再有统计信息被访问或者收集了。
