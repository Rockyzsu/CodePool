 ## Jobs: pausing and resuming crawls

 这个页面主要写暂停爬虫并恢复爬虫的。
 
 ###  job 目录
 设置JOBDIR即可

 ### 如何使用他
 ```
 scrapy crawl somespider -s JOBDIR=crawls/somespider-1
 ```
停止他， 你需要ctrl -c 或者发送一个信号，重启启动
```
scrapy crawl somespider -s JOBDIR=crawls/somespider-1
```

### 获取状态信息
```python
def parse_item(self, response):
    # parse item here
    self.state['items_count'] = self.state.get('items_count', 0) + 1
```
### 持久性的陷阱
#### cookies 过期
如果你暂停你的调度太久的话， cookes可能会过期的。
#### 请求序列化
请求必须是能pickle模块可可序列化的。下面的这个情况就无法工作
```python
def some_callback(self, response):
    somearg = 'test'
    return scrapy.Request('http://www.example.com', callback=lambda r: self.other_callback(r, somearg))

def other_callback(self, response, somearg):
    print "the argument passed is:", somearg
```
上面的这个是使用lamba函数在请求的回调方法中， 不能持久

你可以使用如下
```python
def some_callback(self, response):
    somearg = 'test'
    return scrapy.Request('http://www.example.com', callback=self.other_callback, meta={'somearg': somearg})

def other_callback(self, response):
    somearg = response.meta['somearg']
    print "the argument passed is:", somearg
```

如果你想了解到那些请求没有别序列化， 可以设置SCHEDULER_DEBUG=True来启动调度调试获取更详细的信息.
