__author__ = 'songtao'
# -*- coding: utf-8 -*-

from django.conf.urls import *
from vsa.genericviews import *
from models import *
from forms import *
from .views import *


# from server import views

urlpatterns =[
    url(r'^list/?$',FormListView.as_view(
        form_class=LinkForm,
        model=quicklink,
        template_name='quicklink.html',
        context_object_name="result",
        success_url='/quicklink/list/'
    ),name='quicklink'),
    url(r'update/(?P<pk>\d+)', GenericUpdateView.as_view(
        model=quicklink,
        form_class=LinkForm,
        success_url='/quicklink/list/'
    ), name='updatelink'),

    url(r'del/(?P<pk>\d+)', GenericDelView.as_view(
        model=quicklink,
        success_url='/quicklink/list/'
    ), name='delquicklink'),
    url(r'interface/list/?$',quicklist,name='quicklist'),

]