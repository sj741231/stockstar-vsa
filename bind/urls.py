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
    url(r'domain/?$',FormListView.as_view(
        model=Domain,
        form_class=DomainForm,
        template_name='domainlist.html',
        paginate_by='10',
        success_url='/bind/domain'
    ),name='domainlist'),
    url(r'domian/del/(?P<pk>\d+)', GenericDelView.as_view(
        model=Domain,
        success_url='/bind/domain/'
    ), name='deldomain'),
    url(r'dnsrecord/(?P<zone>\d*)/?$', RecordListView.as_view(), name='dnsrecordlist'),

    url(r'dnsrecord/(?P<zone>\d+)/add/?$', RecordCreateView.as_view(), name='addrecord'),

    url(r'dnsrecord/change/(?P<zone>\d+)/(?P<pk>\d+)/?$', RecordUpdateView.as_view(), name='dnsrecordupdate'),

    url(r'dnsrecord/del/(?P<zone>\d+)/(?P<pk>\d+)/?$', RecordDelView.as_view(), name='delrecord'),
]
