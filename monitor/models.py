# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from vcenter.models import virtualhost

# Create your models here.


class MonitorServer(models.Model):
    name = models.CharField(verbose_name='名称',max_length=100)
    url = models.CharField(verbose_name='地址',max_length=100)
    user = models.CharField(verbose_name='用户',max_length=100)
    password = models.CharField(verbose_name='密码',max_length=100)

    def __unicode__(self):
        return self.name


class MonitorHostDetail(models.Model):
    host = models.ForeignKey(virtualhost)
    monitor_server = models.ForeignKey(MonitorServer)
    monitor_id = models.IntegerField(verbose_name='监控id')
    status = models.BooleanField(default=False)
    check_datatime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.monitor_server.name + '_' + self.host.name
