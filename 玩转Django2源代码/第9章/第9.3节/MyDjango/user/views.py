from django.shortcuts import render
from .form import MyUserCreationForm

# 使用表单实现用户注册
def registerView(request):
    if request.method == 'POST':
        user = MyUserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            tips = '注册成功'
            user = MyUserCreationForm()
    else:
        user = MyUserCreationForm()
    return render(request, 'user.html',locals())