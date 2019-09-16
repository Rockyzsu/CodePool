from haystack import indexes
from .models import Product
# 类名必须为模型名+Index，比如模型Product,则索引类为ProductIndex
class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # 设置模型
    def get_model(self):
        return Product
    # 设置查询范围
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
