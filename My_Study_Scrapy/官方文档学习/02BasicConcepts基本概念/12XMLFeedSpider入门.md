##　XMLFeedSpider
XMLFeedSpider设计用于通过以特定节点名称遍历它们来解析XML Feed。 迭代器可以从：iternodes，xml和html中选择。 由于性能原因，建议使用iternodes迭代器，因为xml和html迭代器一次生成整个DOM，以便解析它。 但是，使用html作为迭代器可能在使用错误的标记解析XML时非常有用。
### iterator
三个值设置
* 'iternodes'：基于正则表达式的快速迭代器
* 'html'：使用Selector的迭代器。 请记住，这使用DOM解析，并且必须加载内存中的所有DOM，这可能是大型Feed的问题
* 'xml'：使用Selector的迭代器。 请记住，这使用DOM解析，并且必须加载内存中的所有DOM，这可能是大型Feed的问题

### itertag 
设置要迭代的节点名字

### namespaces
一个 (prefix,url)元组的列表，
样例
```python
class YourSpider(XMLFeedSpider):

    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    itertag = 'n:url'
    # ...
```
###  adapt_response(response)
一种在蜘蛛中间件到达之前，在蜘蛛开始解析之前收到响应的方法。 它可以在解析之前用于修改响应正文。 此方法接收响应并返回响应（可能相同或相同）。
上面是google翻译的， 说白了就是在response解析前就预处理好。
### parse_node(response, selector)
对于与提供的标签名称（itertag）匹配的节点，将调用此方法。 接收响应和每个节点的选择器。 覆盖此方法是强制性的。 否则你的蜘蛛不会工作。 此方法必须返回一个Item对象，一个Request对象或一个包含它们的迭代。
这个方法就是类似spider的parse方法， 用于返回一个Item，一个Request对象或者其他迭代。
### process_results(response, results)
对由蜘蛛返回的每个结果（项目或请求）调用此方法，并且将返回结果返回到框架核心之前执行所需的最后一次处理，例如设置项目ID。 它收到结果列表和起始于这些结果的响应。 它必须返回结果列表（项目或请求）。
## 样例
```python
from scrapy.spiders import XMLFeedSpider
from myproject.items import TestItem

class MySpider(XMLFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.xml']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = TestItem()
        item['id'] = node.xpath('@id').extract()
        item['name'] = node.xpath('name').extract()
        item['description'] = node.xpath('description').extract()
        return item
```
