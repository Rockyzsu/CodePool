# coding:utf-8

from scrapy.item import Item
from scrapy import Field    # 只能通过x['aa']或者x.get('aa')访问, x.aa无法访问, 除非重写__getattribute__()
from pprint import pformat
from collections import MutableMapping
import six
from scrapy.utils.trackref import object_ref

__all__ = [
    'DictItem',                 # 可被a.b访问属性的DictItem类
]

# ORM 数据库关系对象映射

class BaseItem(object_ref):
    """Base class for all scraped items."""
    pass

class DictItem(MutableMapping, BaseItem):
    fields = {}

    def __init__(self, *args, **kwargs):
        self._values = {}
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            raise KeyError("%s does not support field: %s" %
                (self.__class__.__name__, key))

    def __delitem__(self, key):
        del self._values[key]

    def __getattr__(self, name):
        if name in self.fields:
            raise AttributeError("Use item[%r] to get field value" % name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            raise AttributeError("Use item[%r] = %r to set field value" %
                (name, value))
        super(DictItem, self).__setattr__(name, value)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    __hash__ = BaseItem.__hash__

    def keys(self):
        return self._values.keys()

    def __repr__(self):
        return pformat(dict(self))

    def copy(self):
        return self.__class__(self)

