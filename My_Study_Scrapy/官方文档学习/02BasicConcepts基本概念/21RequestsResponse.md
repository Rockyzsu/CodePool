## 请求和响应
Request和Response这2个类是抓取web的基础类。

### Request objects

#### class scrapy.http.Request(url[, callback, method='GET', headers, body, cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback, flags])
这个类用于构造一个http请求，通常在爬虫里面生成的，被下载器执行，最终生成一个Response。

详细参数
* url: 请求的url
* callback:响应流的回调方法
* method: 请求方法，默认是'GET'
* meta:用于和响应流交互数据
* body:请求body信息
* header:请求头信息
* cookies:cookies信息
    ```python
    request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'})
    request_with_cookies = Request(url="http://www.example.com",
                               cookies=[{'name': 'currency',
                                        'value': 'USD',
                                        'domain': 'example.com',
                                        'path': '/currency'}])
    ```
* encoding:默认是utf-8的
* priority:请求的优先级，影响调度，正数提高优先级，负数降低。
* dont_fileter: 不过滤，默认是False:也就是会过滤掉重复的
* errback:错误的回调
* flags:发送到请求的标志，可用于日志或其他用途。

##### url
请求的url只读的。想改变url使用replace方法。
##### method
请求的方法
##### headers
请求头信息
##### body
请求体信息
##### meta
请求元数据
##### copy()
返回这个请求的copy
##### replace([url, method, headers, body, cookies, meta, encoding, dont_filter, callback, errback])
返回一个对象，新数值覆盖旧的
```python
    def copy(self):
        """Return a copy of this Request"""
        return self.replace()

    def replace(self, *args, **kwargs):
        """Create a new Request with the same attributes except for those
        given new values.
        """
        for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta',
                  'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)
```

### 多个回调方法完成一个item构建
```python
def parse_page1(self, response):
    item = MyItem()
    item['main_url'] = response.url
    request = scrapy.Request("http://www.example.com/some_page.html",
                             callback=self.parse_page2)
    request.meta['item'] = item
    yield request

def parse_page2(self, response):
    item = response.meta['item']
    item['other_url'] = response.url
    yield item
```
这个代码很明白的， 我们要构造的item属性不再一个页面内， 我们需要将第一个页面完成那的item填充一部分属性，
把这个通过meta属性带到下一个回调中， 让下一个回调填充剩余的字段 最终完成对象的赋值工作。

### 使用错误回到方法处理异常
```python
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ErrbackSpider(scrapy.Spider):
    name = "errback_example"
    start_urls = [
        "http://www.httpbin.org/",              # HTTP 200 expected
        "http://www.httpbin.org/status/404",    # Not found error
        "http://www.httpbin.org/status/500",    # server issue
        "http://www.httpbin.org:12345/",        # non-responding host, timeout expected
        "http://www.httphttpbinbin.org/",       # DNS error expected
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    errback=self.errback_httpbin,
                                    dont_filter=True)

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
```
这个代码看着挺吓人， 真正没有啥实质的东西， 我们可以指定errback，对错误进行处理， 不如这里的日志的分类记录

### Request.meta 特定的一些key

* dont_redirect
* dont_retry
* handle_httpstatus_list
* handle_httpstatus_all
* dont_merge_cookies (see cookies parameter of Request constructor)
* cookiejar
* dont_cache
* redirect_urls
* bindaddress
* dont_obey_robotstxt
* download_timeout
* download_maxsize
* download_latency
* download_fail_on_dataloss
* proxy
* ftp_user (See FTP_USER for more info)
* ftp_password (See FTP_PASSWORD for more info)
* referrer_policy
* max_retry_times

## 表单请求对象

### classmethod from_response(response[, formname=None, formid=None, formnumber=0, formdata=None, formxpath=None, formcss=None, clickdata=None, dont_click=False, ...])

* response:一个包含表单的html，有需要填充的字段
* formname:设置表单的名字属性
* formid:表单对应id值设置
* formxapth:第一个匹配的表单
* formcss:第一个匹配的表单
* fromnumber: 第几个表单， 第一个表单编号为0
* clickdata:属性来查找空间中的单击
* formdata:重写表单的数据
* dont_click:如果设置true,表单数据提交不会点击任何元素

### 使用FromRequest 去发送一个http post请求
```python
return [FormRequest(url="http://www.example.com/post/action",
                    formdata={'name': 'John Doe', 'age': '27'},
                    callback=self.after_post)]
```
### 使用FromRequest.from_response()去模拟用户登陆
```python
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
 ```
## 响应流对象

### class scrapy.http.Response(url[, status=200, headers=None, body=b'', flags=None, request=None])
* url:响应的url
* status:响应码
* header:相应头信息
* body:响应体信息
* flags:是一个list
* request:这个响应的对应请求对象

#### url
只读属性，影响流的url。只能用过response.replace改变。

#### status
正数 ， http的状态码。

#### headers
响应的头部信息，类似字典的对象， 你可以使用getlist()获取对应的属性
```python
response.headers.getlist('Set_Cookie')
```

#### body 
响应流的主题， 是bytes对象， 你想获取unicode可以使用TextResponse.text，只读属性
可以使用response.replace修改。

#### meta
是一个快照self.request.meta, 可以通过他将数据从response传递到response流

#### flags
一个宝航响应流标志的列表， 主要用于引擎和日志

#### copy()
翻译一个响应流的copy

#### replace([url, status, headers, body, request, flags, cls])
返回一个响应流的相同成员的对象，可以指定修改。比如response =response.replace(body=response.body.decode('gbk'))

#### urljoin(url)
url:是一个相对的url,本质是urlparse.urljoin(response.url,url)

#### follow(url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding='utf-8', priority=0, dont_filter=False, errback=None)
这个方法接受和初始化一样的参数， 但是这个url可以是相对当前响应流的相对地址，建议使用follow,不使用urljoin方法。


## TextResponse 对象
### class scrapy.http.TextResponse(url[, encoding[, ...]])
* encoding : 编码

#### text
相当于response.body.decode(response.encoding)

#### encoding

具有此响应编码的字符串。通过尝试以下机制来解决编码问题：

* 构造函数编码参数中传递的编码。
* 在内容类型http标头中声明的编码。如果此编码无效（即未知），则忽略它，并尝试下一个解析机制。
* 响应体中声明的编码。的textresponse类不提供任何特殊的功能。然而，这htmlresponse和xmlresponse课呢。
* 通过查看响应体推断出的编码。这是比较脆弱的方法，也是最后一种方法

#### selector 
选择器使用响应流作为目标， 是懒实例化的

#### xpath(query)
快照方法TextREsponse.selector.xpath(query)

#### css(query)
快照方法TextREsponse.selector.css(query)

#### follow(url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding=None, priority=0, dont_filter=False, errback=None)
返回一个新的请求

#### body_ad_unicode()
这个方法和text相同的， 为了向后兼容的方法， 请使用text属性访问即可。 




