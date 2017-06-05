from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from accounts.views import index
from django.conf import settings
from logs.views import test

admin.autodiscover()



urlpatterns = [
    # Examples:
    # url(r'^$', 'jumpserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^__debug__/',include(debug_toolbar.urls)),

    url(r'^$', login_required(index)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^permission/', include('permission.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^servers/',include('server.urls')),
    url(r'^quicklink/',include('quicklink.urls')),
    url(r'^vcenter/',include('vcenter.urls',namespace='vcenter')),
    url(r'^logs/',include('logs.urls',namespace='logs')),
    url(r'^admanage/',include('admanage.urls',namespace='admanage')),
    url(r'^bind/',include('bind.urls',namespace='bind')),
    url(r'^idc/',include('idc.urls',namespace='idc')),
    url(r'^live/',include('live.urls',namespace='live')),
#    url(r'^monitor/',include('monitor.urls',namespace='monitor')),
    url(r'^notify/',include('notify.urls',namespace='notify')),
    url(r'^assets/', include('assets.urls',namespace='assets')),
    url(r'^resources/', include('resources.urls',namespace='resources')),
    url(r'^configmanage/', include('configmanage.urls',namespace='configmanage')),

    url(r'^admin/', admin.site.urls),
    url(r'^rpc/',test,name='test'),
#    url(r'^mbphone/', include('mbphone.urls')),    

]

