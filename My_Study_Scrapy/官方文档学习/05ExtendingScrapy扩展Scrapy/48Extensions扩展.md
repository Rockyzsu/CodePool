## Extension扩展

这个扩展框架提供插入自己的功能到scrapy中去。

### 加载和激活扩展
扩展在启动时通过是劣化扩展类的单个实例来加载和激活，因此所有的扩展初始化代码都必须在类构造函数（__init__）中执行。
设置添加
```json
EXTENSIONS = {
    'scrapy.extensions.corestats.CoreStats': 500,
    'scrapy.extensions.telnet.TelnetConsole': 500,
}
```
### 禁用一个扩展
```json
EXTENSIONS = {
    'scrapy.extensions.corestats.CoreStats': None,
}
```

### 写自己的扩展
每个扩展都是一个python类， 对于扩展重要的点就是from_crawler方法，这个方法接受一个crawler对象，通过这个crawler对象， 你可以访问settings,signals,stats,并且控制crawler的行为。 
如果from_crawler方法抛出一个Not_Configured异常， 这个扩展就是禁用的。否则就是启用的。 


### 样例扩展
这个样例的需求是在爬虫打开，关闭，指定数目的items抓取到都要写一个信息。
```python
import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class SpiderOpenCloseLogging(object):

    def __init__(self, item_count):
        self.item_count = item_count
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

        # instantiate the extension object
        ext = cls(item_count)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s", spider.name)

    def spider_closed(self, spider):
        logger.info("closed spider %s", spider.name)

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        if self.items_scraped % self.item_count == 0:
            logger.info("scraped %d items", self.items_scraped)
```
这个代码整体也是很简单的， from_crawler方法是关键的， 通过crawler对象获取settings, 先进行判定，初始化一个对象，绑定信号。


