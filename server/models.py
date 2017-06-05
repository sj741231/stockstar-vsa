# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class HostGroup(models.Model):
    name = models.CharField(max_length=50,verbose_name=u'主机组')
    description = models.CharField(max_length=200,verbose_name=u'描述')

    def __unicode__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'主机名', unique=True, help_text=u"主机名-ip地址")
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'IP地址')
    hostgroup = models.ForeignKey(HostGroup, verbose_name=u'主机组', blank=True, null=True)

    def __unicode__(self):
        return self.ip


class Event(models.Model):
    user = models.ForeignKey(User)
    host = models.ForeignKey(Host)
    timestamp = models.DateTimeField(auto_now=True)
    log = models.FileField()

    def __unicode__(self):
        return self.user.username + self.host.name
