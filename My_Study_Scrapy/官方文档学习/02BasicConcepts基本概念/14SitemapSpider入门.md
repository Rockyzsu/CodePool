##　SitemapSpider
SitemapSpider允许您通过使用Sitemaps发现URL来抓取站点。
它支持嵌套的站点地图，并从robots.txt发现站点地图URL。
### sitemap_urls
指向要抓取其网址的站点地图的网址列表。
你也可以指向一个robots.txt，它将被解析为从其中提取站点地图URL。
### sitemap_rules
一个(regex,callback)的元组列表。
regex是正则表达式，callback是对应的回调方法，样例使用`sitemap_rules = [('/product/', 'parse_product')]`
### sitemap_follow
应遵循的sitemap的正则表达式列表。 这仅适用于使用指向其他站点地图文件的Sitemap索引文件的网站。
默认情况下，将遵循所有的站点地图。
### sitemap_alternate_links
指定是否应遵循一个网址的备用链接。 这些是在同一个URL块内传递的另一种语言的相同网站的链接。默认是禁用的。

### parse_row(response, row)
这是个核心方法，类似baseSpider的parse方法，返回一个
## 样例1
```python
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
        ('/category/', 'parse_category'),
    ]

    def parse_product(self, response):
        pass # ... scrape product ...

    def parse_category(self, response):
        pass # ... scrape category ...
```
## 样例2
```python
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]
    sitemap_follow = ['/sitemap_shops']

    def parse_shop(self, response):
        pass # ... scrape shop here ...
```