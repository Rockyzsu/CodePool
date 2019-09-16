## SpiderMiddleware爬虫中间件

爬虫中间件是一个钩子框架， 可以自定义设置爬虫处理来出来指定请求

### 激活一个爬虫中间件
```json
SPIDER_MIDDLEWARES = {
    'myproject.middlewares.CustomSpiderMiddleware': 543,
}
```
编号小的先执行process_spider_input方法，编号大的后执行process_spider_input。

编号大的限制性process_spider_output方法，编号小的后执行process_spider_output。

### 写自己的爬虫中间件

### class scrapy.spidermiddlewares.SpiderMiddleware
#### process_spider_input(response, spider)
这个是处理爬虫输入的，这个方法应该返回一个None或者一个异常。

如果返回是一个None，继续处理这个响应，直到所有的中间件处理完毕。

如果触发一个异常， 就停止调用其他中间件的precess_spider_input方法，将会调用请求的错误回调方法，

#### process_spider_output(response, result, spider)
这个是处理爬虫输出的， 返回值只能是可迭代的REquest,dict,Item对象。

#### process_spider_exception(response, exception, spider)
这个方法在process_spider_input,process_spider_output方法的时候出现异常的时候调用

返回值只能是None，或者可迭代的Response,dict,Item对象。 

如果返回None,将会继续处理这个异常， 知道中间件没有处理的时候，异常到达引擎。

如果返回一个可迭代的结果， 就会进入process_spider_output,其他的异常处理不会在执行了。

#### process_start_requests(start_requests, spider)
接受一个可迭代的start_requests参数，必须返回一个可迭代的Request对象。 

