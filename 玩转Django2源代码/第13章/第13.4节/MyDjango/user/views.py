from django.shortcuts import render
# 用户注册界面
def loginView(request):
    title = '用户注册'
    return render(request, 'user.html', locals())

# 注册后回调的页面
from django.http import HttpResponse
def success(request):
    return HttpResponse('注册成功')