## AutoThrottleExtension自动调整扩展
 
### 设计目标

* 不使用默认的下载延迟（0），减轻服务器压力
* 自动优化抓取速度，用户只需要设置最大并发，剩下的这个扩展来完成。
### 它是如何工作的

它自动调正爬虫，发送AUTOTHROTTLE_TARGET_CONCURRENCY 并发请求到每个远程主机。

使用下载等待去计算下载应该延迟时间，大概思路是这样的，等待10s，加入10个并行，那就设置下载延迟为1s


### 调整算法

1. 爬虫启动下载延迟 AUTOTHROTTLE_START_DELAY
2. 在响应流得到的时候，等待时间/并发值作为AUTOTHROTTLE_TARGET_CONCURRENCY
3. 下一个请求得到的时候，计算均值作为下载延迟
4. 出现non-200就不会在调低延迟
5. 下载延迟不能低于DOWNLOAD_DELAY 或者高于AUTOTHROTTLE_MAX_DELAY


### 相关设置

* AUTOTHROTTLE_ENABLE :是否启用，默认False
* AUTOTHROTTLE_START_DELAY:初始的下载延迟，默认是5
* AUTOTHROTTLE_MAX_DELAY:最大的下载延迟，默认60
* AUTOTHROTTLE_TARGET_CORRENCY:默认1
* AUTOTHROTTLE_DEBUG：启动调试，默认False
* CONCURRENT_REQUESTS_PER_DOMAIN:每个域的并发
* CONCURRENT_REQUESTS_PER_IP：每个ip的并发
* DOWNLOAD_DELAY:下载延迟