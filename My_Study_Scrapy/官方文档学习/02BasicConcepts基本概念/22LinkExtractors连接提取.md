## LinkExtractors连接提取

### 内建的连接提取参考
内建的连接提取是LinkExtractor,这个和LxmlLinkExtractor一样的。
```pytho
from scrapy.linkextractors import LinkExtractor
```
### LxmlLinkExtractor
#### class scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow=(), deny=(), allow_domains=(), deny_domains=(), deny_extensions=None, restrict_xpaths=(), restrict_css=(), tags=('a', 'area'), attrs=('href', ), canonicalize=False, unique=True, process_value=None, strip=True)
* allow : 一个正则表达式或者列表，默认匹配所有连接
* deny  : 一个正则表达式或者列表，默认不会过滤任何连接
* allow_domains:指定那些域可以提取
* deny_domains:指定那些域不可以提取
* deny_extension:哪些连接可以被忽略
* restrict_xpath:只有xpath内部的url才可以提取
* restrict_css:只有css内部的url才可以提取
* tags:那些标签可以去提取，默认是a,area
* attrs:tags的那个属性去提取，默认是('href',)
* canonoicalize : 规范每个提取的url,默认是false
* uniique : 是否重复过滤那些提取到的连接
* process_value: 这个是针对attrs的值处理的方法， 默认是lambbda x:x 也就是href属性是啥就是啥地址
    可以使用如下方法修改
    ```python
    <a href="javascript:goToPage('../other/page.html'); return false">Link text</a>
    def process_value(value):
        m = re.search("javascript:goToPage\('(.*?)'", value)
        if m:
            return m.group(1)
    ```
* strip: 是否删除前导和尾随的空白符号。

