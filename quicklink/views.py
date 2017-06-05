from django.shortcuts import render
from django.http.response import HttpResponse
from .models import quicklink
import json

# Create your views here.

def quicklist(request):
    data = [{'name':x.name,'link':x.link} for x in quicklink.objects.all()]
    return HttpResponse(json.dumps(data))



