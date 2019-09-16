from django.shortcuts import render
from django.http import HttpResponse
from .form import *
def index(request):
    # GET请求
    if request.method == 'GET':
        product = ProductForm()
        return render(request, 'data_form.html',locals())
    # POST请求
    else:
        product = ProductForm(request.POST)
        if product.is_valid():
            # 获取网页控件name的数据
            # 方法一
            name = product['name']
            # 方法二
            # cleaned_data将控件name的数据进行清洗，转换成Python数据类型
            cname = product.cleaned_data['name']
            return HttpResponse('提交成功')
        else:
            # 将错误信息输出，error_msg是将错误信息以json格式输出
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())


def model_index(request, id):
    if request.method == 'GET':
        instance = Product.objects.filter(id=id)
        # 判断数据是否存在
        if instance:
            product = ProductModelForm(instance=instance[0])
        else:
            product = ProductModelForm()
        return render(request, 'data_form.html', locals())
    else:
        product = ProductModelForm(request.POST)
        if product.is_valid():
            # 获取weight的数据，并通过clean_weight进行清洗，转换成Python数据类型
            weight = product.cleaned_data['weight']
            # 直接保存到数据库
            # product.save()
            # save方法设置commit=False，生成数据库对象product_db，然后可对该对象的属性值修改并保存
            product_db = product.save(commit=False)
            product_db.name = '我的iPhone'
            product_db.save()
            # save_m2m()方法是保存ManyToMany的数据模型
            #product.save_m2m()
            return HttpResponse('提交成功!weight清洗后的数据为：'+weight)
        else:
            # 将错误信息输出，error_msg是将错误信息以json格式输出
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())