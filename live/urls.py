# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django.conf.urls import *
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from .views import *
from .models import *
from .forms import *
from vsa.genericviews import *

urlpatterns = [

    url(r'list/?$', FormListView.as_view(
        form_class=VideoForm,
        model=video,
        template_name='videosourcelist.html',
        context_object_name="result",
        paginate_by=10,
        success_url='/live/list'
    ), name='videosourcelist'),

    url(r'videosourceupdate/(?P<pk>\d+)', GenericUpdateView.as_view(
        form_class=VideoForm,
        model=video,
        success_url='/live/list'
    ), name='videosourceupdate'),

    url(r'videosource/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=video,
        success_url='/live/list'
    ), name='delvideosource'),
    # url(r'monitor_video/(?P<pk>[0-9]+)/?$',monitor_video,name='monitor_video'),

    url(r'channal/?$', FormListView.as_view(
        form_class=LiveChannelForm,
        model=LiveChannel,
        template_name='livechannel.html',
        context_object_name="result",
        paginate_by=10,
        success_url='/live/channal/'
    ), name='channallist'),

    url(r'channal/(?P<pk>\d+)', GenericUpdateView.as_view(
        form_class=LiveChannelForm,
        model=LiveChannel,
        success_url='/live/channal/'
    ), name='channaledit'),

    url(r'channal/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=LiveChannel,
        success_url='/live/channal'
    ), name='channaldel'),

    url(r'node/?$', FormListView.as_view(
        form_class=LiveNodeForm,
        model=LiveNode,
        template_name='nodelist.html',
        context_object_name="result",
        paginate_by=10,
        success_url='/live/node'
    ), name='nodelist'),

    url(r'node/(?P<pk>\d+)', GenericUpdateView.as_view(
        form_class=LiveNodeForm,
        model=LiveNode,
        success_url='/live/node'
    ), name='nodeedit'),

    url(r'node/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=LiveNode,
        success_url='/live/node'
    ), name='nodedel'),
    url(r'watchvideo/(?P<pk>[0-9]+)/?$', watch_video, name='watchvideo'),
    url(r'mobileplay/(?P<pk>[0-9]+)/?$', mobile_play, name='mobileplay'),
    url(r'player/?$', player, name='player'),

]
