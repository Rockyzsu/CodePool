from django import forms
from .models import *
from django.core.exceptions import ValidationError
# 表单
# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=20, label='名字',)
#     weight = forms.CharField(max_length=50, label='重量')
#     size = forms.CharField(max_length=50, label='尺寸')
#     choices_list = [(i+1, v['type_name']) for i,v in enumerate(Type.objects.values('type_name'))]
#     type = forms.ChoiceField(choices=choices_list, label='产品类型')


# 自定义数据验证函数
def weight_validate(value):
    if not str(value).isdigit():
        raise ValidationError('请输入正确的重量')
# 表单
class ProductForm(forms.Form):
    # 设置错误信息并设置样式
    name = forms.CharField(max_length=20, label='名字',
                           widget=forms.widgets.TextInput(attrs={'class': 'c1'}),
                           error_messages={'required': '名字不能为空'},)
    # 使用自定义数据验证函数
    weight = forms.CharField(max_length=50, label='重量',validators=[weight_validate])
    size = forms.CharField(max_length=50, label='尺寸')
    # 获取数据库数据
    choices_list = [(i+1, v['type_name']) for i,v in enumerate(Type.objects.values('type_name'))]
    # 设置CSS样式
    type = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'type','size':'4'}),
                             choices=choices_list,label='产品类型')

# 数据库表单
class ProductModelForm(forms.ModelForm):
    # 重写ProductModelForm类的初始函数__init__
    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        # 设置下拉框的数据
        type_obj = Type.objects.values('type_name')
        choices_list = [(i + 1, v['type_name']) for i, v in enumerate(type_obj)]
        self.fields['type'].choices = choices_list
        # 初始化字段name
        self.fields['name'].initial = '我的手机'

    # 添加模型外的表单字段
    productId = forms.CharField(max_length=20, label='产品序号', initial='NO1')
    # 模型与表单设置
    class Meta:
        # 绑定模型
        model = Product
        # fields属性是设置转换字段，'__all__'是将全部模型字段转换成表单字段
        # fields = '__all__'
        fields = ['name','weight','size','type']
        # exclude是禁止模型字段转换表单字段
        exclude = []
        # labels设置HTML元素控件的label标签
        labels = {
            'name': '产品名称',
            'weight': '重量',
            'size': '尺寸',
            'type': '产品类型'
        }
        # 定义widgets，设置表单字段的CSS样式
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'c1'}),
        }
        # 定义字段的类型,一般情况下模型的字段会自动转换成表单字段
        field_classes = {
            'name': forms.CharField
        }
        # 帮助提示信息
        help_texts = {
            'name': ''
        }
        # 自定义错误信息
        error_messages = {
            # __all__设置全部错误信息
            '__all__': {'required': '请输入内容',
                         'invalid': '请检查输入内容'},
            # 设置某个字段错误信息
            'weight': {'required': '请输入重量数值',
                        'invalid': '请检查数值是否正确'}
        }

    # 自定义表单字段weight的数据清洗
    def clean_weight(self):
	   # 获取字段weight的值
        data = self.cleaned_data['weight']
        return data+'g'
