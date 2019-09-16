from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# 获取settings.py的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyDjango.settings')
# 定义Celery对象，并将项目配置信息加载到对象中。
# Celery的参数一般以为项目名命名
app = Celery('MyDjango')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# 创建测试任务
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))