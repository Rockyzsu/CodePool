from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['username','email','mobile','qq','weChat']
    # 新增用户时，在个人信息里添加'mobile','qq','weChat'的信息录入
    # 将源码的UserAdmin.fieldsets转换成列表格式
    fieldsets = list(UserAdmin.fieldsets)
    # 修改fieldsets，添加'mobile','qq','weChat'的信息录入
    fieldsets[1] = (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile', 'qq', 'weChat')})