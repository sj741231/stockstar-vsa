__author__ = 'songtao'
#-*-coding=utf8-*-

from django.conf.urls import *
from forms import NotifyUserForm
from vsa.genericviews import FormListView,GenericDelView,GenericUpdateView
from .models import *
from .views import *

#edit by shijin 
from notify import views


urlpatterns = [
    url(r'users/?$',FormListView.as_view(
        form_class=NotifyUserForm,
        model=NotifyUser,
        template_name='notifyuser.html',
        context_object_name="result",
        success_url='/notify/users'
    ),name='notifyusers'),
    url(r'update/(?P<pk>\d+)/?$', GenericUpdateView.as_view(
        model=NotifyUser,
        form_class=NotifyUserForm,
        success_url='/notify/users'
    ), name='updatenotifyuser'),

    url(r'del/(?P<pk>\d+)/?$', GenericDelView.as_view(
        model=NotifyUser,
        success_url='/notify/users'
    ), name='delnotifyusers'),
    url(r'notify/?$',notify,name='notify'),
    url(r'log/?$',FormListView.as_view(
        form_class=NotifyUserForm,
        model=NotifyLog,
        template_name='notifylist.html',
        context_object_name='result',
        success_url=''
    ),name='notifylog'),
#edit by shijin 
    url(r'^smsaduser/$', views.sms_ad_user),
    url(r'^smssender/$', views.sms_ad_send),
    
]