# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''

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

    url(r'ip/list/?$', FormListView.as_view(
        form_class=IpAddressForm,
        model=IpAddress,
        template_name='iplist.html',
        context_object_name="result",
        paginate_by=10,
        success_url='/resources/ip/list/'
    ), name='iplist'),
    url(r'ip/update/(?P<pk>\d+)', GenericUpdateView.as_view(
        model=IpAddress,
        form_class=IpAddress,
        success_url='/resources/ip/list/'
    ), name='updateip'),

    url(r'ip/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=IpAddress,
        success_url='/resources/ip/list/'
    ), name='delip'),
]