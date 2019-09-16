### 内置爬虫中间件

#### DepthMiddleware
##### class scrapy.spidermiddlewares.depth.DepthMiddleware
这个中间件是追踪爬虫深度的，可以限制请求的深度。
* DEPTH_LIMIT: 最大请求深度，0代表不限制
* DEPTH_STAT:是否收集统计信息
* DEPTH_PRIORITY:深度优先级

#### HttpErrorMiddleware
##### class scrapy.spidermiddlewares.httperror.HttpErrorMiddleware
过滤掉错误的http响应
* HTTPERROR_ALLOWED_CODES:允许码，默认是[]
* HTTPERROR_ALLOW_ALL:默认是false,

如果你想你的爬虫处理404响应，设置如下即可
```python
class MySpider(CrawlSpider):
    handle_httpstatus_list = [404]
```
#### OffsiteMiddleware
##### class scrapy.spidermiddlewares.offsite.OffsiteMiddleware
过滤指定域之外的请求
设置爬虫的allowed_domains即可
如果请求设置了dont_filter属性，这个offsite中间件会允许这个这个请求通过的。 

#### RefererMiddleware
##### class scrapy.spidermiddlewares.referer.RefererMiddleware

这个中间件会在新的请求的头信息中添加Refer头信息
可以使用response.request.headers["Refer]
* REFERER_ENABLED:是否启用引用中间件， 默认是是True
* REferer_policy: 引用策略设置


具体的值，直接去官方网址看看即可。

* "scrapy-default" (default)	    scrapy.spidermiddlewares.referer.DefaultReferrerPolicy
*  “no-referrer”	                scrapy.spidermiddlewares.referer.NoReferrerPolicy
* “no-referrer-when-downgrade”	    scrapy.spidermiddlewares.referer.NoReferrerWhenDowngradePolicy
* “same-origin”	                    scrapy.spidermiddlewares.referer.SameOriginPolicy
* “origin”	                        scrapy.spidermiddlewares.referer.OriginPolicy
* “strict-origin”	                scrapy.spidermiddlewares.referer.StrictOriginPolicy
* “origin-when-cross-origin”	    scrapy.spidermiddlewares.referer.OriginWhenCrossOriginPolicy
* “strict-origin-when-cross-origin”	scrapy.spidermiddlewares.referer.StrictOriginWhenCrossOriginPolicy
* “unsafe-url”	                    scrapy.spidermiddlewares.referer.UnsafeUrlPolicy

* class scrapy.spidermiddlewares.referer.DefaultReferrerPolicy ：  这个是默认的，除了file:///,s3：这些是没有设置refer信息， http,https都会设置信息的。
* class scrapy.spidermiddlewares.referer.NoReferrerPolicy ： 这个就是不引用了。
* class scrapy.spidermiddlewares.referer.NoReferrerWhenDowngradePolicy ：  同时是https的请求带，https->http不带refer信息
* class scrapy.spidermiddlewares.referer.SameOriginPolicy  ： 同一个域的携带， 不一个不带。
* class scrapy.spidermiddlewares.referer.OriginPolicy ： 只有ascii序列化的请求客户端发送， 其他的不发送
* class scrapy.spidermiddlewares.referer.StrictOriginWhenCrossOriginPolicy  : 只有ascii序列化的请求客户端， 且请求是https->https这种都是加密的带， 其他的不带。
* class scrapy.spidermiddlewares.referer.UnsafeUrlPolicy ： 这个scrapy还没有实现。 

#### UrlLengthMiddleware
##### class scrapy.spidermiddlewares.urllength.UrlLengthMiddleware
这个中间件就是用来限制url长度的
ULRLENGTH_LIMIT:设置运行抓取的最大url长度。 超过这个长度都会被过滤掉。 

