__author__ = 'songtao'
# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.contrib.admin.views.decorators import staff_member_required
from vsa.genericviews import GenericDelView,GenericDelView,FormListView,GenericUpdateView

from .views import *
from .models import *
from .forms import SwitchForm
# from server import views

urlpatterns = [
    url(r'switch/list/?$', FormListView.as_view(
        model = Switch,
        form_class = SwitchForm,
        template_name = 'switchlist.html',
        success_url= '/assets/switch/list',
        # paginate_by=15,
    ), name='switchlist'),

    url(r'switch/update/(?P<pk>\d+)/?$', GenericUpdateView.as_view(
        model = Switch,
        form_class = SwitchForm,
        success_url= '/assets/switch/list',

    ), name='switchupdate'),

    url(r'^switch/del/(?P<pk>\d+)/?$', GenericDelView.as_view(
        model = Switch,
        success_url= '/assets/switch/list',

    ), name='switchdel'),



]


