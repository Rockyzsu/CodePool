### 嵌套加载器
```html
<footer>
    <a class="social" href="http://facebook.com/whatever">Like Us</a>
    <a class="social" href="http://twitter.com/whatever">Follow Us</a>
    <a class="email" href="mailto:whatever@example.com">Email Us</a>
</footer>
```
不使用嵌套的
```python
loader = ItemLoader(item=Item())
# load stuff not in the footer
loader.add_xpath('social', '//footer/a[@class = "social"]/@href')
loader.add_xpath('email', '//footer/a[@class = "email"]/@href')
loader.load_item()
```
使用嵌套的
```
loader = ItemLoader(item=Item())
# load stuff not in the footer
footer_loader = loader.nested_xpath('//footer')
footer_loader.add_xpath('social', 'a[@class = "social"]/@href')
footer_loader.add_xpath('email', 'a[@class = "email"]/@href')
# no need to call footer_loader.load_item()
loader.load_item()
```
从官方的样例上可以看出来。嵌套加载器可以让你的代码更简洁，更清晰，提取结构更明了。

### 重用和扩展item加载器
```python
from scrapy.loader.processors import MapCompose
from myproject.ItemLoaders import ProductLoader

def strip_dashes(x):
    return x.strip('-')

class SiteSpecificLoader(ProductLoader):
    name_in = MapCompose(strip_dashes, ProductLoader.name_in)
```
这个就是继承重用， ProductLoader我们可能写了一堆处理函数。 想再次基础上加一些处理函数呢。 
把代码粘贴过来。然后把多的函数加上去吗。 那样多都比啊。 直接使用继承即可。

### 内置的处理器介绍
上面我们也介绍了内置的处理器。
这些处理器非常重要，这里还是在说明下。

### class scrapy.loader.processors.Identity
```python
class Identity(object):

    def __call__(self, values):
        return values
```
这个代码就是给啥值就返回啥。 这个处理器也是默认的输入和输出处理器。

样例
```python
>>> from scrapy.loader.processors import Identity
>>> proc = Identity()
>>> proc(['one', 'two', 'three'])
['one', 'two', 'three']
```

### class scrapy.loader.processors.TakeFirst
```python
class TakeFirst(object):

    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value
```
这个代码就是遍历一个可迭代的对象，找到第一个不是None，并且不是''的就返回。
样例
```python
>>> from scrapy.loader.processors import TakeFirst
>>> proc = TakeFirst()
>>> proc(['', 'one', 'two', 'three'])
'one'
```

### class scrapy.loader.processors.Join(separator=u' ')
```python
class Join(object):

    def __init__(self, separator=u' '):
        self.separator = separator

    def __call__(self, values):
        return self.separator.join(values)
```
这个代码初始化的时候就是设置了一个分割符号str类型的。 调用的时候本质是调用string.join方法。将可迭代对象合并起来。
```python
>>> from scrapy.loader.processors import Join
>>> proc = Join()
>>> proc(['one', 'two', 'three'])
u'one two three'
>>> proc = Join('<br>')
>>> proc(['one', 'two', 'three'])
u'one<br>two<br>three'
```

### class scrapy.loader.processors.Compose(*functions, **default_loader_context)
```python
class Compose(object):

    def __init__(self, *functions, **default_loader_context):
        self.functions = functions
        self.stop_on_none = default_loader_context.get('stop_on_none', True)
        self.default_loader_context = default_loader_context

    def __call__(self, value, loader_context=None):
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        for func in wrapped_funcs:
            if value is None and self.stop_on_none:
                break
            value = func(value)
        return value

```
这个代码相对复杂点，在构造函数中，function是函数列表，default_loader_context是一个字典，
获取字典中是否有stop_on_none，没有就是采用默认的true。设置默认的加载器上下文。
在调用函数中，如果有就加载上下文，使用MergeDict合并默认加载上下文和传递过来的加载器上下文。
否则就采用默认的加载上下文。接下类就是遍历函数列表wrapped_funcs，一个一个的处理。
相当于我们的value,经过第一个func有输出有，传递给第二个func处理，在给下一个func处理。一直到最后一个func执行完毕，就返回value，类似管道技术。
```python
>>> from scrapy.loader.processors import Compose
>>> proc = Compose(lambda v: v[0], str.upper)
>>> proc(['hello', 'world'])
'HELLO'
>>> proc([None，'hello', 'world'])
```
这里调用proc(['hello', 'world'])，value=['hello', 'world'],接着`if value is None and self.stop_on_none`判断，接下里执行了`value = func(value)`,value=hello,判断None,然后在upper下就得到了HELLO

### class scrapy.loader.processors.MapCompose(*functions, **default_loader_context)
```python
class MapCompose(object):

    def __init__(self, *functions, **default_loader_context):
        self.functions = functions
        self.default_loader_context = default_loader_context

    def __call__(self, value, loader_context=None):
        values = arg_to_iter(value)
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        for func in wrapped_funcs:
            next_values = []
            for v in values:
                next_values += arg_to_iter(func(v))
            values = next_values
        return values
```
这个代码基本上compose差的不多。就在for循环里面有差别的。具体代码分析看下下面的一个样例
```python
>>> def filter_world(x):
...     return None if x == 'world' else x
...
>>> from scrapy.loader.processors import MapCompose
>>> proc = MapCompose(filter_world, unicode.upper)
>>> proc([u'hello', u'world', u'this', u'is', u'scrapy'])
[u'HELLO, u'THIS', u'IS', u'SCRAPY']
```
values开始是[u'hello', u'world', u'this', u'is', u'scrapy']，for遍历函数，内层for遍历values,
那么第一个v就是'hello',经过func处理就是'hello'，调用了arg_to_iter将字符串hello转化为['hello'],+=到next_values上去，接下来处理world，经过filter_word得到None,经过arg_to_iter得到[],+=后next_values就是['hello'],接下来的'this','is','scrapy'都是这样处理下，就得到了['hello','this','is','scrapy']，这样外层的一个func执行完毕，接下来就是以另一个函数upper了。那最终结果就是[u'HELLO, u'THIS', u'IS', u'SCRAPY']

### class scrapy.loader.processors.SelectJmes(json_path)
```python
class SelectJmes(object):
    """
        Query the input string for the jmespath (given at instantiation),
        and return the answer
        Requires : jmespath(https://github.com/jmespath/jmespath)
        Note: SelectJmes accepts only one input element at a time.
    """
    def __init__(self, json_path):
        self.json_path = json_path
        import jmespath
        self.compiled_path = jmespath.compile(self.json_path)

    def __call__(self, value):
        """Query value for the jmespath query and return answer
        :param value: a data structure (dict, list) to extract from
        :return: Element extracted according to jmespath query
        """
        return self.compiled_path.search(value)
```
这个代码没有实质的代码，就是调用了jmespath的方法，感觉和re有点想，compile,然后search。
详细的可以去这里看看[https://github.com/jmespath/jmespath.py#jmespath](https://github.com/jmespath/jmespath.py#jmespath),有几个样例，看看就明白了。
```python
>>> from scrapy.loader.processors import SelectJmes, Compose, MapCompose
>>> proc = SelectJmes("foo") #for direct use on lists and dictionaries
>>> proc({'foo': 'bar'})
'bar'
>>> proc({'foo': {'bar': 'baz'}})
{'bar': 'baz'}
>>> proc2 =SelectJmes("foo.bar")
>>> proc({'foo': {'bar': 'baz'}})
'bar'
```
### 其他的
scrapy提供了6个基本的处理器，当然我们可以自己写，也可以组合使用这6个达到我们的目的。
```python
>>> import json
>>> proc_single_json_str = Compose(json.loads, SelectJmes("foo"))
>>> proc_single_json_str('{"foo": "bar"}')
u'bar'
>>> proc_json_list = Compose(json.loads, MapCompose(SelectJmes('foo')))
>>> proc_json_list('[{"foo":"bar"}, {"baz":"tar"}]')
[u'bar']
```
第一种情况，我们处理的是一个join字符串，所以肯定需要一个json.loads的方法转化为json对象，json对象的提取需要使用Selectmes。组合一下就可以了。'{"foo": "bar"}'==>{"foo": "bar"}==>'bar'

第二种情况：数据处理流程基本如下： '[{"foo":"bar"}, {"baz":"tar"}]'==>[{"foo":"bar"}, {"baz":"tar"}]==>['bar']+[]

### 总结

item加载器就是为填充item而存在的。 其实我们可以自己这样写，item=Product(),item["name"]=response.css("div p::text"),这种方式去自己构造我们的item。但是这种方式没有使用item加载器优雅，且item加载器可以设置写输入输出处理器，方便数据的处理。使用继承也能提高我们代码的重用率。相信大家水平的提高，会越来月爱上item加载器的使用的。

你可以看下不使用加载器的代码：[https://github.com/zhaojiedi1992/quotesbot](https://github.com/zhaojiedi1992/quotesbot)
使用加载器的代码： [https://github.com/zhaojiedi1992/quotesbot_v2](https://github.com/zhaojiedi1992/quotesbot_v2)
这2个代码都不是我自己写的， 第一个就是直接把官方网址的那个demo fork过来的。 第二个就是在scrapyhub上创建一个portial项目，配置完毕下载的scrapy的代码提交到github上的。
大家可以借鉴下第二种写法。可扩展性很高。