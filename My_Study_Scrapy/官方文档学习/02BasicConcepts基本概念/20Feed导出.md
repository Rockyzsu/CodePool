## feed导出

这是最常见的一种功能，当需要实现爬虫是能妥善保存数据，通常，这意味着抓取到的数据生成一个i“导出文件”（俗称“出口饲料”）被其他系统消耗。

Scrapy提供此开箱即用的接口，它可以让你使用多个序列化格式和存储后端。

支持的序列化格式： 
* JSON
* JSON lines
* CSV
* XML

通过FEED_EXPORTERS设置，可以扩展支持
* JSON
* JSON LINES
* CSV
* XML
* PICKLE
* MARSHAL
* STORAGES

其中storages有支持几种
* 本地文件系统
* ftp
* s3
* 标准输出（终端）

### Storage URI PARAMETER
* %(time)s - feed被创建的时间
* %(name)s - 爬虫名字
样例：
```
ftp://user:password@ftp.example.com/scraping/feeds/%(name)s/%(time)s.json
s3://mybucket/scraping/feeds/%(name)s/%(time)s.json
```
注意ftp的格式，带上用户名和密码
