from .models import Product
from .serializers import ProductSerializer

# APIView 方式生成视图
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
class product_class(APIView):
    # get 请求
    def get(self, request):
        queryset = Product.objects.all()
        # 分页查询，需要在settings.py设置REST_FRAMEWORK属性
        pg = PageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = ProductSerializer(instance=page_roles, many=True)
        # serializer = ProductSerializer(instance=queryset, many=True) # 全表查询
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)
    # post 请求
    def post(self, request):
        # 获取请求数据
        serializer = ProductSerializer(data=request.data)
        # 数据验证
        if serializer.is_valid():
            # 保存到数据库
            serializer.save()
            # 返回对象Response由Django Rest Framework实现，status是设置响应状态码
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 普通函数方式生成视图
from rest_framework.decorators import api_view
@api_view(['GET', 'POST'])
def product_def(request, pk):
    if request.method == 'GET':
        queryset = Product.objects.filter(id=pk).all()
        serializer = ProductSerializer(instance=queryset, many=True)
        # 返回对象Response由Django Rest Framework实现
        return Response(serializer.data)
    elif request.method == 'POST':
        # 获取请求数据
        serializer = ProductSerializer(data=request.data)
        # 数据验证
        if serializer.is_valid():
            # 保存到数据库
            serializer.save()
            # 返回对象Response由Django Rest Framework实现，status是设置响应状态码
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)