__author__ = 'songtao'
#-*-coding=utf8-*-

from django.conf.urls import *
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .views import *



urlpatterns = [
    url(r'^maclog/?$',IpMacList.as_view(),name='maclog'),
    url(r'^maclog/count/?$',getmacreglogcount,name='maclogcount'),
    url(r'^rev_user_authlog/?$',revinterface,name='revinterface')
]