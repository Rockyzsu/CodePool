## Logging 日志

## 日志级别
* logging.CRITICAL
* logging.ERROR
* logging.WARNING
* logging.INFO
* loggin.DEBUG

### 如何写日志
```python
import logging 
logging.warning("this is a warning")
```
### 爬虫中记录日志
```python

import scrapy

class MySpider(scrapy.Spider):

    name = 'myspider'
    start_urls = ['https://scrapinghub.com']

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
```
### 命令行选项
* --logfile FILE
* --loglevel
* --nolog

### scrapy.utils.log module
```python
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)
```