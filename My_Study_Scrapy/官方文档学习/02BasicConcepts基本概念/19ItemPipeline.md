## item管道
爬虫的parse方法会返回一个item对象，发送到Item pipeline

item Pipeline 作用
* 清洗数据
* 验证数据
* 去重
* 持久化（入库，或者写文件等）

### 写自己的item管道
每个item管道都是一个类，继承下默认的item管道，实现下几个方法就可以了 。
#### process_item(self, item, spider)
这个方法在每次item经过管道的时候调用，用于处理item。返回值是item,deferred队形，或者抛出一个DropItem异常。丢弃的item不会进行接下来的管道了。

#### open_spider(self, spider)
这个方法只有在爬虫打开的时候调用

#### close_spider(self, spider)
这个方法在爬虫关闭的时候调用

#### from_crawler(cls, crawler)
这个类根据一个爬虫者对象创建一个管道对象，爬虫者对象提供给管道对象访问爬虫的属性。

### Item管道的样例
```python
from scrapy.exceptions import DropItem

class PricePipeline(object):

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)
```
这个pricePipeline管道类，只提供了一个process_item的方法，对item属性进行修改，对特定的数据进行丢弃。

### 使用Item管道写item到json文件中 
```python
import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
```
这个item管道实用性还是非常高的，很有学习意义。open_spider这个方法只有在爬虫被打开的时候触发，close_spider方法只有在爬虫被关闭的时候才触发，process_item这个方法在爬虫parse方法中return 一个item触发。这个item管道类完成的功能就是在爬虫打开的时候创建一个jl文件，获取到item的时候写到js文件中， 最后爬虫关闭的时候把文件关闭了。 

上面的样例只是提供一个怎么使用item管道的样例，如果你想把item写到json文件中，建议使用Feed Exports功能。

### 使用Item管道写item到mongodb数据库中
```python
import pymongo

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
```
这个比上面的那个jsonPipeline复杂了点， 但是open_spider,close_spider,process_item都是一样的， 主要是剩下的2个方法都是啥。
from_crawler 就是从crawler对象创建一个管道对象，crawler有设置信息，我们可以通过crawler获取我们必要的配置。在__init__方法里面配合完成类属性的设置。
open_spider 就是根据设置打开数据库。process_item就是入库操作， close_spider就是关闭数据库连接。

### 将item延期

这个例子告诉我们如何从process_item()如何返回一个item延期对象。它使用splash来渲染item URL的屏幕截图。管道对本地运行的splash实例发出请求。下载请求并推迟回调后，它将项保存到文件，并将文件名添加到项中。
```python
import scrapy
import hashlib
from urllib.parse import quote


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""

    SPLASH_URL = "http://localhost:8050/render.png?url={}"

    def process_item(self, item, spider):
        encoded_item_url = quote(item["url"])
        screenshot_url = self.SPLASH_URL.format(encoded_item_url)
        request = scrapy.Request(screenshot_url)
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)
        return dfd

    def return_item(self, response, item):
        if response.status != 200:
            # Error happened, return item.
            return item

        # Save screenshot to file, filename will be hash of url.
        url = item["url"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        filename = "{}.png".format(url_hash)
        with open(filename, "wb") as f:
            f.write(response.body)

        # Store filename in item.
        item["screenshot_filename"] = filename
        return item
```
### 过滤重复
```python
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
```
这个就是一个去重的管道了 ，仅仅这一个是没有用的，做完去重后就没有了。 没有做持久化处理，这部扯犊子吗。这个需要和其他的管道配合使用的。

### 激活Item管道组件
```
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}
```
在设置文件中，定义了好几个pipelines,可以把去重的放前面（编号小点），后面放一个持久化的管道即可。这样做可以保证各个管道职责单一， 组合小功能完成大功能。
