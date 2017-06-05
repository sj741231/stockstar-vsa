__author__ = 'songtao'
#-*-coding=utf8-*-

from django.conf.urls import *
from django.contrib.admin.views.decorators import staff_member_required
# from accounts.models import User,UserGroup
from django.contrib.auth.models import User,Group

from django.views.generic import UpdateView
from forms import UserForm,UserGroupForm
from vsa.genericviews import FormListView,GenericDelView,GenericUpdateView
from .views import *


from django.contrib.auth.views import *


urlpatterns = [
    #user login interface
    # url(r'^/?$', 'login'),
    url(r'^$', mbphone_views.home, name='home'),
    url(r'^home1/$', mbphone_views.home1, name='home1'),


]