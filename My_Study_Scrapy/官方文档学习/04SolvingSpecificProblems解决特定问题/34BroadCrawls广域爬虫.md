## Broad Crawls 广域爬虫

广域爬虫的特点

* 他们抓取许多域（通常是无界的）而不是一组特定的站点
* 他们不一定要抓取域名才能完成，因为这样做是不切实际的（或不可能），而是按时间或爬网页数来限制抓取
* 它们在逻辑上更简单（与具有许多提取规则的非常复杂的蜘蛛相反），因为数据经常在单独的阶段中被后处理
* 他们同时抓取多个域，这使得他们可以通过不受任何特定站点约束（每个站点缓慢爬取以尊重礼貌，但许多站点并行抓取）来实现更快的爬网速度

### 增加并发
```
CONCURRENT_REQUESTS = 100
```

### 增加twisted io 线程池最大值
```
REACTOR_THREADPOOL_MAXSIZE = 20
```

### 降低日志级别
```
LOG_LEVEL = 'INFO'
```
### 禁用cookies

```
COOKIES_ENABLED =False
```

### 禁用重试
```
RETRY_ENABLED = False
```
### 降低下载超时时间
```
DOWNLOAD_TIMEOUT = 15 
```

### 禁用重定向
```
REDIRECT_ENABLED = False
```

### 启用ajax抓取
```
AJAXCRAWL_ENABLED = True
```

