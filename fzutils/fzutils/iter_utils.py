# coding:utf-8

"""
可迭代对象utils
"""

# itemgetter 常用用法eg: sorted([{'index': 2}, {'index': 1}], key=itemgetter('index'))
from operator import itemgetter
from toolz.itertoolz import groupby

__all__ = [
    'group_by',                     # 通过key function 给list分组
    'filter_iterable_obj',          # 过滤可迭代对象
]

def group_by(key, seq):
    """ 通过key function 给list分组
    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> group_by(len, names)  # doctest: +SKIP
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}
    >>> iseven = lambda x: x % 2 == 0
    >>> group_by(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
    {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}
    Non-callable keys imply grouping on a member.
    >>> group_by('gender', [{'name': 'Alice', 'gender': 'F'},
    ...                    {'name': 'Bob', 'gender': 'M'},
    ...                    {'name': 'Charlie', 'gender': 'M'}]) # doctest:+SKIP
    {'F': [{'gender': 'F', 'name': 'Alice'}],
     'M': [{'gender': 'M', 'name': 'Bob'},
           {'gender': 'M', 'name': 'Charlie'}]}
    See Also:
        countby
    """
    return groupby(key, seq)

def filter_iterable_obj(func, iterable_obj):
    '''
    过滤可迭代对象
        simple use:
        a = [
            {
                'id': 1,
            },{
                'id': 2,
            }
        ]
        b = list(filter_iterable_obj(lambda x: x.get('id') > 1, a))
        print(b)
    :param func: 筛选函数
    :param iterable_obj: 可迭代对象
    :return:
    '''
    return filter(func, iterable_obj)