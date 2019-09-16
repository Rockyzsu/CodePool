## Stats Collection 状态收集

### 公共状态收集使用

```python
class ExtensionThatAccessStats(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
```

### 内存状态收集者
#### class scrapy.statscollectors.MemoryStatsCollector
* spider_stats:状态信息

### DummyStatsCollector
#### class scrapy.statscollectors.DummyStatsCollector
这个统计类，啥也不做，但是是非常有效的，提高性能。
