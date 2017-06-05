#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
 
 
def home(request):
    return render(request, 'mbphone/home.html')

def home1(request):
    string = "测试新项目！"
    return render(request, 'mbphone/home1.html', {'string': string})