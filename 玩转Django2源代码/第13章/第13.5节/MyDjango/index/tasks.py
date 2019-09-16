from celery import shared_task
from .models import *
import time
# 带参数的分布式任务
@shared_task
def updateData(product_id, value):
    Product.objects.filter(id=product_id).update(weight=value)

# 该任务用于执行定时任务
@shared_task
def timing():
    now = time.strftime("%H:%M:%S")
    with open("E:\\output.txt", "a") as f:
        f.write("The time is " + now)
        f.write("\n")
        f.close()