# 定义用户登录表单类
from django import forms
from captcha.fields import CaptchaField
class CaptchaTestForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    captcha = CaptchaField()
