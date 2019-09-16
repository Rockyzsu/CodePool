from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# 使用login_required和permission_required分别对用户登录验证和用户权限验证
@login_required(login_url='/user/login.html')
@permission_required(perm='index.visit_Product', login_url='/user/login.html')
def index(request):
	return render(request, 'index.html', locals())

# # 使用函数has_perm实现装饰器permission_required功能
# from django.shortcuts import render, redirect
# @login_required(login_url='/user/login.html')
# def index(request):
# 	user = request.user
# 	if user.has_perm('index.visit_Product'):
# 		return render(request, 'index.html', locals())
# 	else:
# 		return redirect('/user/login.html')