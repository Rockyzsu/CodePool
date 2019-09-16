## Debugging Spiders调试爬虫

```python
import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = (
        'http://example.com/page1',
        'http://example.com/page2',
        )

    def parse(self, response):
        # collect `item_urls`
        for item_url in item_urls:
            yield scrapy.Request(item_url, self.parse_item)

    def parse_item(self, response):
        item = MyItem()
        # populate `item` fields
        # and extract item_details_url
        yield scrapy.Request(item_details_url, self.parse_details, meta={'item': item})

    def parse_details(self, response):
        item = response.meta['item']
        # populate more `item` fields
        return item
```
### 使用Parse Command
```cmd
$ scrapy parse --spider=myspider -c parse_item -d 2 <item_url>
[ ... scrapy log lines crawling example.com spider ... ]

>>> STATUS DEPTH LEVEL 2 <<<
# Scraped Items  ------------------------------------------------------------
[{'url': <item_url>}]

# Requests  -----------------------------------------------------------------
[]
```
我个人不用这个方法的。

### 使用 Scrapy Shell

```
scrapy shell url
response.xpath('//h1[@class="fn"]')
```
这个调试方法是我个人比较喜欢的， 我个人使用css选择器，使用浏览器先调试功能先获取到css，使用shell 测试下这个css 查询语句正确就写到爬虫代码里面。

### Open in Browser 

有时候我们发现打开浏览器访问和我们使用爬虫的结果不一致的时候，可以使用这个去比较下。
```python
from scrapy.utils.response import open_in_browser

def parse_details(self, response):
    if "item name" not in response.body:
        open_in_browser(response)
```


### Logging 日志

```python
def parse_details(self, response):
    item = response.meta.get('item', None)
    if item:
        # populate more `item` fields
        return item
    else:
        self.logger.warning('No item received for %s', response.url)
```
注意这里使用self.logger.warning 打印日志，确保settings的日志级别设置低于这个等级。
