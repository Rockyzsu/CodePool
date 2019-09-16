# scrapy入门
## 提取数据
打开命令终端，输入如下命令
```cmd
scrapy shell 'http://quotes.toscrape.com/page/1/'
```
*注意：window下网址使用双引用起来而不是单引号*

我们可以看到如下的信息
```
[ ... Scrapy log here ... ]
2016-09-19 12:09:27 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7fa91d888c90>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x7fa91d888c10>
[s]   spider     <DefaultSpider 'default' at 0x7fa91c8af990>
[s] Useful shortcuts:
[s]   shelp()           Shell help (print this help)
[s]   fetch(req_or_url) Fetch request (or URL) and update local objects
[s]   view(response)    View response in a browser
>>>
```
如果你的不是上面的输出的话， 检查下你的**ipython**解释器安装了没有，对你没有看错，是IPython,你可以使用如下命令安装ipython。
``` cmd
python -m pip install ipython
```
我们可以使用如下代码提取标题文本
```python
>>> response.css('title::text').extract()
['Quotes to Scrape']
```
我们分析下这个代码是怎么能提取到数据的吧。
我们先定位到scrapy.http\response.__init__.py文件，找到css方法，可以看到css方法对TextResponse有效,我们在定位到scrapy.http\response.text.py找到css方法，看到如下代码
``` python
    def css(self, query):
        return self.selector.css(query)
        @property
    def selector(self):
        from scrapy.selector import Selector
        if self._cached_selector is None:
            self._cached_selector = Selector(self)
        return self._cached_selector
```
我们看到调用的css方法，时调用了selector的css方法， 我们定位到这个selecotr去， 可以看到这个对象是一个Selector对象，我们定位过去看看。
``` python
class Selector(_ParselSelector, object_ref):
```
我们这里可以看到Selector是继承了_ParselSelector，我们定位过去看看_ParselSelector。
```python
    def css(self, query):
        """
        Apply the given CSS selector and return a :class:`SelectorList` instance.

        ``query`` is a string containing the CSS selector to apply.

        In the background, CSS queries are translated into XPath queries using
        `cssselect`_ library and run ``.xpath()`` method.
        """
        return self.xpath(self._css2xpath(query))
```

从上面的代码我们可以看出来css的方法调用了xpath的方法了， 先使用css2xpath将我们的css查询转成xpath的查询， 然后调用了xpath查询。


我们默认使用extract方法提取到的一般是个[]，如果我们想提取单个数值的话可以使用extract_first方法，不用担心我们使用索引获取而发生异常。

## 爬虫中提取数据
上面我们的爬虫只是把网页源码给拿到了，显然这不是我们所要的。 我们需要特定的去提取网页的有用数据。我们修改我们的爬虫为如下代码：
```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
```
## 存储爬虫的结果数据
```cmd
scrapy crawl quotes -o quotes.json
```
再工程目录下，运行上面的命令，我们可以看到在工程目录下有quotes.json文件生成，内容如下：
```json
[
{"text": "\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d", "author": "Albert Einstein", "tags": ["change", "deep-thoughts", "thinking", "world"]},
{"text": "\u201cIt is our choices, Harry, that show what we truly are, far more than our abilities.\u201d", "author": "J.K. Rowling", "tags": ["abilities", "choices"]},
{"text": "\u201cThere are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.\u201d", "author": "Albert Einstein", "tags": ["inspirational", "life", "live", "miracle", "miracles"]},
{"text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d", "author": "Jane Austen", "tags": ["aliteracy", "books", "classic", "humor"]},
{"text": "\u201cImperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.\u201d", "author": "Marilyn Monroe", "tags": ["be-yourself", "inspirational"]},
{"text": "\u201cTry not to become a man of success. Rather become a man of value.\u201d", "author": "Albert Einstein", "tags": ["adulthood", "success", "value"]},
{"text": "\u201cIt is better to be hated for what you are than to be loved for what you are not.\u201d", "author": "Andr\u00e9 Gide", "tags": ["life", "love"]},
{"text": "\u201cI have not failed. I've just found 10,000 ways that won't work.\u201d", "author": "Thomas A. Edison", "tags": ["edison", "failure", "inspirational", "paraphrased"]},
{"text": "\u201cA woman is like a tea bag; you never know how strong it is until it's in hot water.\u201d", "author": "Eleanor Roosevelt", "tags": ["misattributed-eleanor-roosevelt"]},
{"text": "\u201cA day without sunshine is like, you know, night.\u201d", "author": "Steve Martin", "tags": ["humor", "obvious", "simile"]},
{"text": "\u201cThis life is what you make it. No matter what, you're going to mess up sometimes, it's a universal truth. But the good part is you get to decide how you're going to mess it up. Girls will be your friends - they'll act like it anyway. But just remember, some come, some go. The ones that stay with you through everything - they're your true best friends. Don't let go of them. Also remember, sisters make the best friends in the world. As for lovers, well, they'll come and go too. And baby, I hate to say it, most of them - actually pretty much all of them are going to break your heart, but you can't give up because if you give up, you'll never find your soulmate. You'll never find that half who makes you whole and that goes for everything. Just because you fail once, doesn't mean you're gonna fail at everything. Keep trying, hold on, and always, always, always believe in yourself, because if you don't, then who will, sweetie? So keep your head high, keep your chin up, and most importantly, keep smiling, because life's a beautiful thing and there's so much to smile about.\u201d", "author": "Marilyn Monroe", "tags": ["friends", "heartbreak", "inspirational", "life", "love", "sisters"]},
{"text": "\u201cIt takes a great deal of bravery to stand up to our enemies, but just as much to stand up to our friends.\u201d", "author": "J.K. Rowling", "tags": ["courage", "friends"]},
{"text": "\u201cIf you can't explain it to a six year old, you don't understand it yourself.\u201d", "author": "Albert Einstein", "tags": ["simplicity", "understand"]},
{"text": "\u201cYou may not be her first, her last, or her only. She loved before she may love again. But if she loves you now, what else matters? She's not perfect\u2014you aren't either, and the two of you may never be perfect together but if she can make you laugh, cause you to think twice, and admit to being human and making mistakes, hold onto her and give her the most you can. She may not be thinking about you every second of the day, but she will give you a part of her that she knows you can break\u2014her heart. So don't hurt her, don't change her, don't analyze and don't expect more than she can give. Smile when she makes you happy, let her know when she makes you mad, and miss her when she's not there.\u201d", "author": "Bob Marley", "tags": ["love"]},
{"text": "\u201cI like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.\u201d", "author": "Dr. Seuss", "tags": ["fantasy"]},
{"text": "\u201cI may not have gone where I intended to go, but I think I have ended up where I needed to be.\u201d", "author": "Douglas Adams", "tags": ["life", "navigation"]},
{"text": "\u201cThe opposite of love is not hate, it's indifference. The opposite of art is not ugliness, it's indifference. The opposite of faith is not heresy, it's indifference. And the opposite of life is not death, it's indifference.\u201d", "author": "Elie Wiesel", "tags": ["activism", "apathy", "hate", "indifference", "inspirational", "love", "opposite", "philosophy"]},
{"text": "\u201cIt is not a lack of love, but a lack of friendship that makes unhappy marriages.\u201d", "author": "Friedrich Nietzsche", "tags": ["friendship", "lack-of-friendship", "lack-of-love", "love", "marriage", "unhappy-marriage"]},
{"text": "\u201cGood friends, good books, and a sleepy conscience: this is the ideal life.\u201d", "author": "Mark Twain", "tags": ["books", "contentment", "friends", "friendship", "life"]},
{"text": "\u201cLife is what happens to us while we are making other plans.\u201d", "author": "Allen Saunders", "tags": ["fate", "life", "misattributed-john-lennon", "planning", "plans"]}
]
```
## 存储结果输出源码分析
我们上面使用了json格式的导出。我们就去源码看看吧。源码在scrapy.exporters.py的JsonItemExporter里面。
```python
class JsonItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file
        # there is a small difference between the behaviour or JsonItemExporter.indent
        # and ScrapyJSONEncoder.indent. ScrapyJSONEncoder.indent=None is needed to prevent
        # the addition of newlines everywhere
        json_indent = self.indent if self.indent is not None and self.indent > 0 else None
        kwargs.setdefault('indent', json_indent)
        kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.first_item = True

    def _beautify_newline(self):
        if self.indent is not None:
            self.file.write(b'\n')

    def start_exporting(self):
        self.file.write(b"[")
        self._beautify_newline()

    def finish_exporting(self):
        self._beautify_newline()
        self.file.write(b"]")

    def export_item(self, item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(b',')
            self._beautify_newline()
        itemdict = dict(self._get_serialized_fields(item))
        data = self.encoder.encode(itemdict)
        self.file.write(to_bytes(data, self.encoding))
```
我们可以看到我们使用json导出方式，提供者是JsonItemExporter，有start_exporting，finish_exporting，export_item这几个方法的。当然其他的导出方法基本上都有这几个方法，只是方法内部有差异而已。
## 追踪链接
修改我们的爬虫代码为如下内容
```python
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
```
上面我们使用了respons提取到下一页的链接地址，然后使用follow函数去请求下一页了。
当然我们也可以使用如下代码去追踪下一页的
```python
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```
这个地方使用了urljoin函数合并出一个url地址，官方推荐使用resposne.follow这种方法的，这个是支持绝对和相对路径的，使用起来也是非常方便的。

## 使用爬虫参数
其实我们有时候爬取网址的时候，这个url需要接受参数才能确定的时候，我们就需要使用如下方法去使用爬虫参数：
``` cmd
scrapy crawl quotes -o quotes-humor.json -a tag=humor
```

修改我们的爬虫为如下代码
``` python
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```
scrapy 如果给爬虫指定 -a tag=humor， 我们的爬虫类会自动执行如下代码self.tag=humor代码。
我们可以去源码看看吧。
在scrapy.spiders.__init__.py文件的Spider类中有如下代码：
```python
    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
```
最为核心的就是那个`self.__dict__.update(kwargs)`这句代码了。 通过参数去更新类属性。
而在爬虫的子类中我们可以看到类似如下的代码
```python
class CrawlSpider(Spider):

    rules = ()

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()
```
我们发现，子类的初始化先调用了父类的初始化方法，那么我们通过命令端指定的参数属性和值就被设置到self上了，我们可以在init方法里面去使用这个外部传递的参数了。