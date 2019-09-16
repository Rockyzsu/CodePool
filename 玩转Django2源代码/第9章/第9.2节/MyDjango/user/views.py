import random
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# 找回密码
def findPassword(request):
    button = '获取验证码'
    new_password = False
    if request.method == 'POST':
        username = request.POST.get('username', 'root')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(username=username)
        # 用户不存在
        if not user:
            tips = '用户' + username + '不存在'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                # 发送验证码并将验证码写入session
                button = '重置密码'
                tips = '验证码已发送'
                new_password = True
                VerificationCode = str(random.randint(1000, 9999))
                request.session['VerificationCode'] = VerificationCode
                user[0].email_user('找回密码', VerificationCode)
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'user.html', locals())