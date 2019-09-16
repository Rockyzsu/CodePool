from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
#
# # @login_required(redirect_field_name='login')
# @login_required(login_url='/user/login.html')
def index(request):
	return render(request, 'index.html', locals())