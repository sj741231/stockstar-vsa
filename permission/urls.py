__author__ = 'songtao'
#-*-coding=utf8-*-

from django.conf.urls import *

from forms import PermForm
from vsa.genericviews import FormListView,GenericDelView,GenericUpdateView
from .views import *

urlpatterns = [
    url(r'perm/?$',FormListView.as_view(
        form_class=PermAddForm,
        model=User_Host,
        template_name='permuser.html',
        context_object_name="result",
        # paginate_by=10,
        success_url='/permission/perm'
    ),name='perm'),
    url(r'perm/update/(?P<pk>\d+)/?$', GenericUpdateView.as_view(
        model=User_Host,
        form_class=PermAddForm,
        success_url='/permission/perm'
    ), name='updateperm'),

    url(r'perm/del/(?P<pk>\d+)/?$', GenericDelView.as_view(
        model=User_Host,
        success_url='/permission/perm'
    ), name='delperm'),
    url(r'remote_add_perm/(?P<pk>[0-9]+)/?$',operate_user_perm,name='remote_add_perm'),
    url(r'user_perminfo/(?P<pk>[0-9]+)/?$',user_perm_info,name='user_perminfo'),
    url(r'refresh_perm/(?P<pk>[0-9]+)/?$',refresh_user_perm,name='refresh_perm'),
    url(r'refresh_host_key/(?P<pk>[0-9]+)/?$',refresh_host_key,name='refresh_host_key'),
    url(r'multadd/?$',multadduserperm,name='multadd'),
    url(r'index/?$',UserPermIndexView.as_view(),name='userperm'),
    url(r'list/(?P<userid>[0-9]+)/?$',UserPermListView.as_view(),name='userpermlist'),
    url(r'del/(?P<pk>[0-9]+)/?$',GenericDelView.as_view(
        model=UserPerm,
        success_url='list'
    ),name='del_perm'),
    url(r'addpem/(?P<pk>[0-9]+)/?$',remote_add_perm,name='addpem'),
    url(r'userperm/add/?$',add_permission,name='permissionadd'),

]