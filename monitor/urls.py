# -*- coding: utf-8 -*-


__author__ = 'songtao'

from django.conf.urls import *
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required

from django.core.urlresolvers import reverse,reverse_lazy
from views import *
from models import *
from .forms import *
from vsa.genericviews import *

urlpatterns = [
    url(r'list/?$',FormListView.as_view(
        model=MonitorServer,
        form_class=MonitorServerForm,
        template_name='monitorlist.html',
        paginate_by='10',
        success_url='/monitor/list'
    ),name='monitorlist'),
    url(r'del/(?P<pk>\d+)', GenericDelView.as_view(
        model=MonitorServer,
        success_url='/monitor/list/'
    ), name='monitordel'),

    url(r'check_monitor',CheckMonitorView.as_view(),name='check_all')
]
