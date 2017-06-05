__author__ = 'songtao'
# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from vsa.genericviews import *
from models import *
from .views import *



# from server import views

urlpatterns =[

    url(r'server/?$',login_required(ListView.as_view(
        model=host,
        template_name='servers.html',
        context_object_name="result",
    )),name='serverlist'),

    url(r'server/detail/(?P<pk>\d+)', DetailView.as_view(
        model=host,
        template_name='hostdetail.html',
    ), name='serverdetail'),

    url(r'interface/list/?$',leftlist,name='leftlist'),

    url(r'vm/?$',login_required(ListView.as_view(
        model=virtualhost,
        template_name='vmlist.html',
        context_object_name="result",
    )),name='vmlist'),

    url(r'vm/detail/(?P<pk>\d+)', login_required(DetailView.as_view(
        model=virtualhost,
        template_name='vmdetail.html',
    )), name='vmdetail'),

    url(r'datacenter/(?P<pk>\d+)',DatacenterListView.as_view(),name='datacentervms'),
    url(r'^$',VcenterDetail.as_view(),name='index'),


]