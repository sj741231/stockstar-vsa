__author__ = 'songtao'
#-*-coding=utf8-*-

from django.conf.urls import *

from .views import *

urlpatterns = [

    url(r'switchbackup/(?P<pk>[0-9]+)/?$',backup_view,name='switch_backup'),

]