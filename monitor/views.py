from django.shortcuts import render

from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.utils.translation import ugettext as _
from vcenter.models import virtualhost
from zabbix_api import zabbix




class CheckMonitorView(View):
    template_name = 'check.html'
    zabbix_object = zabbix()

    def get(self,request):
        hosts = virtualhost.objects.filter(ip__isnull=False)
        m_server =[]
        for host in hosts:
            print host.name
            if self.zabbix_object.host_get(hostip=host.ip):
                print host.ip
                m_server.append(host)
        return render(request,self.template_name,locals())
