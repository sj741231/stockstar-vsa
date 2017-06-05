# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

from models import Host
import json
from models import HostGroup
from permission.tasks import add_perm

# Create your views here.

class MyView(View):

    def get(self,requst,*args,**kwargs):
        return  HttpResponse('hello world!')


def hostlist(request):
    try:
        username = request.GET['username']
    except:
        return HttpResponse('username not found')
    try:
        user = User.objects.get(username=username)
        h_list = user.host_set.all()
        h_list = serialize('json',h_list)
        # h_list = Host.objects.filter(manager=user).values_list('id','name')
        return HttpResponse(h_list)
    except:
        return HttpResponse('user does not found in database')


@login_required()
def host_users(request,pk):
    host = get_object_or_404(Host,pk=pk)
    users = []
    for perm_users in host.user_host_set.all():
        users.append(perm_users.user)
    return render(request,'host_users.html',locals())


def host_count(request):
    data = json.dumps({'host': Host.objects.all().count()})
    return HttpResponse(data)


@login_required()
def host_push_user(request,pk):
    host = get_object_or_404(Host,pk=pk)
    for p in host.user_host_set.all():
        add_perm.delay(username=p.user,ip=str(host.ip))
    return HttpResponse("<script> alert('" + u'推送用户中!' + "');window.location.href='/servers/host'</script>")