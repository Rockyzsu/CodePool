## Item Exporters 导出

### 使用itemExporters 导出的样例
```python
from scrapy import signals
from scrapy.exporters import XmlItemExporter

class XmlExportPipeline(object):

    def __init__(self):
        self.files = {}

     @classmethod
     def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('%s_products.xml' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
```
具体的可以参考我写的一个： [http://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_python_005_scrapy.html](http://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_python_005_scrapy.html)

### 序列化字段
#### 定义一个序列化在字段定义的时候
```python
import scrapy

def serialize_price(value):
    return '$ %s' % str(value)

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field(serializer=serialize_price)
```
#### 重写序列化字段方法
```python
from scrapy.exporter import XmlItemExporter

class ProductXmlExporter(XmlItemExporter):

    def serialize_field(self, field, name, value):
        if field == 'price':
            return '$ %s' % str(value)
        return super(Product, self).serialize_field(field, name, value)
```


### class scrapy.exporters.BaseItemExporter(fields_to_export=None, export_empty_fields=False, encoding='utf-8', indent=0)
* fields_to_export: 那些字段需要导出
* export_empty_fields:那些字段需要导出
* encoding: 编码
* indent:缩进

#### export_item(item)
导出给定的item,这个方法必须被子类实现

#### serialize_field(field, name, value)
返回序列换的结果。 你可以重写这个方法， 

#### start_exporting()
开始导出方法

#### finish_exporting()
导出进程结束的时候的信号， 

#### fields_to_export
那些字段需要导出。 默认是None,None代表所有字段

#### export_empty_fields
是否导出空的字段。 默认是False,

#### encoding 
设置编码， 这个经常需要改的。 

#### indent 
设置缩进的。 
* indent=None没有缩进
* indent<=0 每个item一行， 没有缩进
* indent>0 每个item在自己的行， 根据提供的数字缩进

### class scrapy.exporters.XmlItemExporter(file, item_element='item', root_element='items', **kwargs)
导出格式为xml的。 
* root_element:根的名字
* item_element：节点的名字

### class scrapy.exporters.CsvItemExporter(file, include_headers_line=True, join_multivalued=', ', **kwargs)
导出item格式，如果设置了fields_to_export这个属性设置了，就只导出这几列，不过export_empty_field属性是如何设置的。
* include_header_line: 导出行头
* join_multivalued : 分隔符号

### class scrapy.exporters.PickleItemExporter(file, protocol=0, **kwargs)
导出item为pickle格式

### class scrapy.exporters.PprintItemExporter(file, **kwargs)
美化打印结果的

### class scrapy.exporters.JsonItemExporter(file, **kwargs)
以json格式导出

### class scrapy.exporters.JsonLinesItemExporter(file, **kwargs)
json lines 格式导出
