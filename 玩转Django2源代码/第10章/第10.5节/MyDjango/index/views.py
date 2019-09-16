from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *

# 首页
def index(request):
	return render(request, 'index.html', locals())

# 购物车
def ShoppingCarView(request):
	return render(request, 'ShoppingCar.html', locals())

# 分页功能
def paginationView(request, page):
	# 获取数据表index_product全部数据
	Product_list = Product.objects.all()
	# 设置每一页的数据量为3
	paginator = Paginator(Product_list, 3)
	try:
		pageInfo = paginator.page(page)
	except PageNotAnInteger:
		# 如果参数page的数据类型不是整型，则返回第一页数据
		pageInfo = paginator.page(1)
	except EmptyPage:
		# 用户访问的页数大于实际页数，则返回最后一页的数据
		pageInfo = paginator.page(paginator.num_pages)
	return render(request, 'pagination.html', locals())