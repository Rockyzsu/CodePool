from django.shortcuts import render,redirect
from .models import Product, Type
# Create your views here.
def index(request):
    return render(request, 'index.html')

