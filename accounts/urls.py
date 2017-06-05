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
    url(r'^login/?$', login_view, name="login"),
    url(r'^index/?$', index, name="accounts_index"),
    url(r'^logout/?$', logout, name="logout"),
    url(r'^register/?$', register, name="regist"),
    url(r'^change_passwd/?$', change_pass, name="change_passwd"),
    url(r'^userlist/?$',FormListView.as_view(
        model=User,
        form_class=UserForm,
        template_name='userlist.html',
        context_object_name = 'result',
        success_url='/accounts/userlist',
    ),name='userlist'),
    url(r'^update_user/(?P<pk>[\w-]+)$',GenericUpdateView.as_view(
        model=User,
        form_class=UserForm,
        success_url='/accounts/userlist/'
    ),name='useredit'),
    url(r'^del_user/(?P<pk>[\w-]+)$',GenericDelView.as_view(
        model=User,
        success_url='/accounts/userlist'
    ),name='deluser'),
    url(r'^usergrouplist/?$',FormListView.as_view(
        model=Group,
        form_class=UserGroupForm,
        template_name='usergrouplist.html',
        paginate_by=25,
        success_url='/accounts/usergrouplist/',
        context_object_name = 'result',
    ),name='usergrouplist'),
    url(r'^edit_usergroup/(?P<pk>[\w-]+)$', GenericUpdateView.as_view(
        template_name = 'usergroupedit.html',
        model=Group,
        form_class=UserGroupForm,
        success_url='/accounts/usergrouplist/'
    ), name='editusergroup'),
    url(r'^del_usergroup/(?P<pk>[\w-]+)$',staff_member_required(GenericDelView.as_view(
        model=Group,
        success_url='/accounts/usergrouplist'
    )),name='delusergroup'),
    url(r'interface/user/_count/?$',user_count,name="user_count"),
    url(r'^reset/password_reset/$', password_reset, name='reset_password_reset'),
    url(r'^reset/password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/?$',password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/?$',password_reset_complete,name='password_reset_complete'),
    url(r'^adminresetpassword/(?P<pk>[0-9]+)/?$',adminresetuserpassword,name='adminresetuserpassword'),
    url(r'^send_pk/(?P<pk>[0-9]+)/?$',send_pk,name='send_pk'),

]