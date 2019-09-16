from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import CaptchaTestForm
# 用户登录
def loginView(request):
    if request.method == 'POST':
        form = CaptchaTestForm(request.POST)
        # 验证表单数据
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username):
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        tips = '登录成功'
                else:
                    tips = '账号密码错误，请重新输入'
            else:
                tips = '用户不存在，请注册'
    else:
        form = CaptchaTestForm()
    return render(request, 'user.html', locals())

# ajax接口，实现动态验证验证码
from django.http import JsonResponse
from captcha.models import CaptchaStore
def ajax_val(request):
    if request.is_ajax():
        # 用户输入的验证码结果
        response = request.GET['response']
        # 隐藏域的value值
        hashkey = request.GET['hashkey']
        cs = CaptchaStore.objects.filter(response=response, hashkey=hashkey)
        # 若存在cs，则验证成功，否则验证失败
        if cs:
            json_data = {'status':1}
        else:
            json_data = {'status':0}
        return JsonResponse(json_data)
    else:
        json_data = {'status':0}
        return JsonResponse(json_data)