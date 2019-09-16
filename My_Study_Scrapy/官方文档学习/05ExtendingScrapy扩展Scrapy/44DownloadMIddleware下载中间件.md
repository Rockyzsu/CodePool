## DownloadMIddleware下载中间件

下载中间件是介与请求和响应处理中间的一个钩子框架。

### 激活下载中间件
```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
}
```
这些中间件是有顺序的，按照数值进行排序，处理请求流，小的先process_request ，然后大的处理，响应流是反向的。

如果想禁用系统的下载下载中间件，可以采取如下操作
```
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
```
### 写自己的下载器
#### class scrapy.downloadermiddlewares.DownloaderMiddleware
##### process_request(request, spider)
这个方法在每个请求通过下载中间件的时候调用

返回值只能是None,Response object ,Request object 或者Raise IgnoreRequest

如果返回的是一个Response对象，不会在被其他的process_request和process_exception方法处理
而process_response这个方法总是被调用在每个响应

如果返回一个Request对象， scrapy 会停止process_request 方法，重新调度返回请求，一旦新的请求执行，中间链process_response方法会调用

如果触发一个IgnoreRequest异常， 那么这个中间件的的对应的process_exception（其他下载中间件的对应方法不调用）方法就会被调用，如果这个异常方法里面没哟处理异常， 就会触发Request.errback方法就会被调用。如果没有在errback回调方法里面没有处理错误，就会忽略（这个点和其他的异常是不太一样的）

#####  process_response(request, response, spider)

这个方法只能返回一个Response对象，Request对象，或者Raise a IgnoreRequest异常

如果返回一个Response对象，这个响应会被下一个中间件的process_response方法调用， 知道所有的中间件的process_response方法处理完毕

如果返回一个Request对象，就停止中间件链处理，返回的请求被重新调度。

如果触发一个IgnoreRequest异常，Request.errback错误回调方法就会被执行，如果没有处理这个异常， 这个异常就会被忽略（和其他异常不一样的）

##### process_exception(request, exception, spider)
这个方法在下载处理或者process_request抛出异常的时候执行。

这个方法返回值应该是None,Response object 或者一个Request对象。

如果返回None,scrapy 会继续处理这个异常，执行其他的processs_exception方法，知道没有中间件方法可用

如果返回一个Request方法，会被重新调度，停止process_exception方法，