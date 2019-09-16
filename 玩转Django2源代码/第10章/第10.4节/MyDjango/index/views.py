from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages

# 首页
def index(request):
	return render(request, 'index.html', locals())

# 购物车
def ShoppingCarView(request):
	return render(request, 'ShoppingCar.html', locals())

# 消息提示
def messageView(request):
	# 信息添加方法一
	messages.info(request, '信息提示')
	messages.success(request, '信息正确')
	messages.warning(request, '信息警告')
	messages.error(request, '信息错误')
	# 信息添加方法二
	messages.add_message(request, messages.INFO, '信息提示')
	return render(request, 'message.html', locals(), RequestContext(request))