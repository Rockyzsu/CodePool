## Exception异常
### DropItem
丢弃item异常
### CloseSpider
关闭爬虫异常
### DontCloseSpider
这个异常会触发一个spider_idle的信号，去阻止爬虫关闭

### IgnoreRequest
这个异常会在，调度器和下载器中间件重复，忽略了url请求

### NotConfigured
没有配置异常

### NotSupported
在新功能不被支持的时候触发
