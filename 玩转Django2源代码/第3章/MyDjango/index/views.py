from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello world")

# 带变量的URL的视图函数
def mydate(request, year, month, day):
    return HttpResponse(str(year) +'/'+ str(month) +'/'+ str(day))

# 参数name的URL的视图函数
def myyear(request, year):
    return render(request, 'myyear.html')

# 参数为字典的URL的视图函数
def myyear_dict(request, year, month):
    return render(request, 'myyear_dict.html',{'month':month})