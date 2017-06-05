__author__ = 'songtao'
# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.contrib.admin.views.decorators import staff_member_required
from vsa.genericviews import GenericDelView,GenericDelView,FormListView,GenericUpdateView

from .views import *
from .models import *
from .forms import *

# from server import views

urlpatterns = [
    url(r'^grouprelation/?$', FormListView.as_view(
        model = GroupReleation,
        form_class = GroupReleationForm,
        template_name = 'grouprelation.html',
        success_url= '/admanage/grouprelation',
        # paginate_by=15,
    ), name='grouprelation'),

    url(r'^grouprelation/update/(?P<pk>\d+)/?$', GenericUpdateView.as_view(
        model = GroupReleation,
        form_class = GroupReleationForm,
        success_url= '/admanage/grouprelation',

    ), name='grouprelation_update'),

    url(r'^grouprelation/del/(?P<pk>\d+)/?$', GenericDelView.as_view(
        model = GroupReleation,
        success_url= '/admanage/grouprelation',
    ), name='grouprelation_del'),

    url(r'grouprelation/upload/xls/?$', upload_group_from_xls,name='xls_update'),

    url(r'aduserfile/?$',AdUserFileView.as_view(
        success_url='/admanage/aduserfile'
    ), name='aduserfile'),

    url(r'aduserfile/del/(?P<pk>\d+)/?$',GenericDelView.as_view(
        model=AdUserfile,
        success_url='/admanage/aduserfile'
    ),name='aduserfile_del'),

    url(r'aduserfile/push/(?P<pk>\d+)',push_add_aduser,name="push_add_aduserfile"),

    url(r'^addaduser/logs?$', ListView.as_view(
        model = AdAddUserLog,
        template_name = 'adadduserlog.html',
        # paginate_by=15,
    ), name='add_log'),
    url(r'custom_result/?$',staff_member_required(ListView.as_view(
        model=AdAddUserLog,
        template_name='result.html',
    )),name='custom_result'),

]


