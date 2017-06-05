__author__ = 'songtao'
# -*- coding: utf-8 -*-

from django.conf.urls import *
from vsa.genericviews import *
from .views import *
from models import *
from forms import *


# from server import views

urlpatterns =[
    url(r'host/?$',FormListView.as_view(
        form_class=HostForm,
        model=Host,
        template_name='hostlist.html',
        context_object_name="result",
        success_url='/servers/host'
    ),name='host'),
    url(r'host/update/(?P<pk>\d+)', GenericUpdateView.as_view(
        model=Host,
        form_class=HostForm,
        success_url='/servers/host/'
    ), name='updatehost'),

    url(r'host/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=Host,
        success_url='/servers/host/'
    ), name='delhost'),
    url(r'hostgroup/?$',FormListView.as_view(
        form_class=HostGroupForm,
        model=HostGroup,
        template_name='hostgroup.html',
        context_object_name="result",
        success_url='/servers/hostgroup'
    ),name='hostgroup'),

    url(r'hostgroup/update/(?P<pk>\d+)', GenericUpdateView.as_view(
        model=HostGroup,
        form_class=HostGroupForm,
        success_url='/servers/hostgroup/'
    ), name='updatehostgroup'),

    url(r'hostgroup/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=HostGroup,
        success_url='/servers/hostgroup/'
    ), name='delhostgroup'),

    url(r'event/?$',FormListView.as_view(
        form_class=EventForm,
        model=Event,
        paginate_by='50',
        queryset=Event.objects.all().order_by('-id'),
        template_name='event.html',
        context_object_name="result",
        success_url='/servers/event'
    ),name='event'),

    url(r'host_users/(?P<pk>\d+)',host_users,name='host_users'),
    url(r'interface/hosts/_count/?$',host_count,name="hosts_count"),

]