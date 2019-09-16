## Items

item就是用于将我们抓取的数据转化为一个类。items类提供有类似字典的访问方式。

###  定义Items

```python
import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
```
上面我们就定义了一个Product的类，继承了Item类，有几个字段。last_updated这个字段还指定了序列化方法。
后续对这个类只能使用这几个字段，无法有其他字段。

### 创建item对象
```python
In [7]: product= Product(name="Desktop Pc",price=1000)

In [9]: print (product)
{'name': 'Desktop Pc', 'price': 1000}

In [10]: type(product)
Out[10]: __main__.Product
```
创建item对象和python的其他类创建是一样的。没啥特别的。

### 获取字段值
```python
>>> product['name']
Desktop PC
>>> product.get('name')
Desktop PC

>>> product['price']
1000

>>> product['last_updated']
Traceback (most recent call last):
    ...
KeyError: 'last_updated'

>>> product.get('last_updated', 'not set')
not set

>>> product['lala'] # getting unknown field
Traceback (most recent call last):
    ...
KeyError: 'lala'

>>> product.get('lala', 'unknown field')
'unknown field'

>>> 'name' in product  # is name field populated?
True

>>> 'last_updated' in product  # is last_updated populated?
False

>>> 'last_updated' in product.fields  # is last_updated a declared field?
True

>>> 'lala' in product.fields  # is lala a declared field?
False
```
使用起来和字典是一样的感觉，
### 设置字段值
```python
>>> product['last_updated'] = 'today'
>>> product['last_updated']
today

>>> product['lala'] = 'test' # setting unknown field
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```
也是和字典一样的。

其实在E:\ZhaojiediProject\github\scrapy\scrapy\item.py文件中，我们看出来如下代码：

```python
class Item(DictItem):
    pass
class DictItem(MutableMapping, BaseItem):
class BaseItem(object_ref):
    """Base class for all scraped items."""
    pass
```
可以看出来，Item实际上继承了object_ref,MutableMapping ,所以说有类似自动的操作。

### 访问所有值

```python
>>> product.keys()
['price', 'name']

>>> product.items()
[('price', 1000), ('name', 'Desktop PC')]
```
### 转化和copy等操作

```python
>>> product2 = Product(product) #使用一个对象构造另一个对象
>>> print product2
Product(name='Desktop PC', price=1000)

>>> product3 = product2.copy()  #复制
>>> print product3
Product(name='Desktop PC', price=1000)

>>> dict(product) # 转化为一个dict
{'price': 1000, 'name': 'Desktop PC'}

>>> Product({'name': 'Laptop PC', 'price': 1500}) # 根据一个字段构造一个对象
Product(price=1500, name='Laptop PC')

>>> Product({'name': 'Laptop PC', 'lala': 1500}) #类没有的字段是不可以的。
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```
其实在item.py中有如下代码
```python
    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                (self.__class__.__name__, key))
```
可以看出来， 只有key在类的fields里面，才可以设置，没有就直接抛出异常了。

