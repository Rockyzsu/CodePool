from django.http import HttpResponse
from .tasks import updateData
def index(request):
	# 传递参数并执行异步任务
	updateData.delay(10, '140g')
	return HttpResponse("Hello Celery")