from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib.auth.models import Permission
from django.contrib.auth import login, authenticate, logout

# 用户登录
def loginView(request):
    tips = '请登录'
    title = '用户登录'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if MyUser.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    # 登录当前用户
                    login(request, user)
                return redirect('/')
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    return render(request, 'user.html', locals())

# 用户注册
def registerView(request):
    title = '用户注册'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if MyUser.objects.filter(username=username):
            tips = '用户已存在'
        else:
            user = MyUser.objects.create_user(username=username, password=password)
            user.save()
            # 添加权限
            permission = Permission.objects.filter(codename='visit_Product')[0]
            user.user_permissions.add(permission)
            return redirect('/user/login.html')
    return render(request, 'user.html', locals())

# 退出登录
def logoutView(request):
    logout(request)
    return redirect('/')
