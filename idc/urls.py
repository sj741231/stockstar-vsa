# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django.conf.urls import *
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from views import *
from models import *
from .forms import *
from vsa.genericviews import *

urlpatterns = [
    url(r'^$', index, name='idcindex'),
    url(r'idc/?$', login_required(IdcFormListView.as_view(
        form_class=IdcForm,
        model=Idc,
        template_name='idc/idc_list.html',
        # success_url='/idc/idc',
        context_object_name="idcs",
        paginate_by=10
    )), name='idclist'),
    url(r'update_idc/(?P<pk>[\w-]+)$', GenericUpdateView.as_view(
        model=Idc,
        form_class=IdcForm,
        success_url='/idc/idc'
    ), name='idcedit'),
    url(r'idc/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=Idc,
        # template_name='idc/confirm_delete.html',
        success_url='/idc/idc/'
    ), name='delidc'),

    url(r'racklist/?$', FormListView.as_view(
        form_class=RackForm,
        model=Rack,
        template_name='rack.html',
        context_object_name="result",
        paginate_by=10,
        success_url='/idc/racklist'
    ), name='racklist'),

    url(r'rack/update/(?P<pk>\d+)', GenericUpdateView.as_view(
        model=Rack,
        form_class=RackForm,
        success_url='/idc/racklist/'
    ), name='updaterack'),

    url(r'rack/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=Rack,
        success_url='/idc/racklist/'
    ), name='delrack'),




    url(r'rackslist/?$', FormListView.as_view(
        form_class=RacksForm,
        model=Racks,
        template_name='racks.html',
        context_object_name="result",
        paginate_by=10,
        success_url='/idc/rackslist'
    ), name='rackslist'),

    url(r'racks/update/(?P<pk>\d+)', GenericUpdateView.as_view(
        model=Racks,
        form_class=RacksForm,
        success_url='/idc/rackslist/'
    ), name='updateracks'),

    url(r'racks/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=Racks,
        success_url='/idc/rackslist/'
    ), name='delracks'),

    # url(r'index/?$','index'),
    # url(r'windows/?$','windows_list',name='windows'),
    # url(r'linux/?$','linux_list',name='linux'),
    # url(r'^tunnel/(?P<sys_type>\w+)/(?P<hostip>((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))))/?$', 'tunnel'),
    # url(r'^newrdp/?$','rdp',name='rdp'),
    # url(r'^ssh/?$','ssh',name='ssh'),

]
