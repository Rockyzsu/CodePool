##　CSVFeedSpider
 这个类和XMLFeedSpider是相似的， 这个是处理csv文档的，每次处理一行， 核心方法是parse_row
### delimiter
设定csv文档的分隔符，默认是“,“,这个是英文的逗号。 
###  quotechar
引号的符号， 默认是双引号。

### headers
一个csv文件的列头。
### parse_row(response, row)
这是个核心方法，类似baseSpider的parse方法，返回一个
## 样例
```python
from scrapy.spiders import CSVFeedSpider
from myproject.items import TestItem

class MySpider(CSVFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    quotechar = "'"
    headers = ['id', 'name', 'description']

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)

        item = TestItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']
        return item
```
