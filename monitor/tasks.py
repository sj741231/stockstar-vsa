# -*-coding=utf8-*-
import os
import sys

from vsa.celery import app
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()
from .models import MonitorServer,MonitorHostDetail
from zabbix_api import zabbix
from vcenter.models import host,virtualhost

@app.task(name="check_monitor_host")
def check_monitor_host(m_id):
    monitorserver = MonitorServer.objects.get(id=m_id)
    za_server = zabbix(url=monitorserver.url,user=monitorserver.user,passwd=monitorserver.password)
    for host in virtualhost.objects.all():
        if host.ip:
            monitorid = za_server.host_get(host.ip)
            if monitorid :
                MonitorHostDetail.objects.update_or_create(host=host,monitor_server=monitorserver,monitor_id=monitorid)
    pass