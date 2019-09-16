from django import template
# 注册过滤器
register = template.Library()
# 声明并定义过滤器
@register.filter
def myreplace(value, agrs):
    oldValue = agrs.split(':')[0]
    newValue = agrs.split(':')[1]
    return value.replace(oldValue, newValue)
