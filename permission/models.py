# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from server.models import Host, HostGroup
from vcenter.models import virtualhost


# Create your models here.


class User_Host(models.Model):
    user = models.OneToOneField(User, verbose_name=u'用户', null=True, blank=True,unique=True)
    host = models.ManyToManyField(Host, verbose_name=u'主机', blank=True)
    hostgroup = models.ManyToManyField(HostGroup, verbose_name=u'主机组', blank=True)
    description = models.CharField(max_length=255, verbose_name=u'描述', blank=True)

    def __unicode__(self):
        return self.user.username


# class Usergroup_Hostgroup(models.Model):
#     usergroup = models.OneToOneField(Group,null=True,blank=True,unique=True)
#     host = models.ManyToManyField(Host, blank=True)
#     hostgroup = models.ManyToManyField(HostGroup, blank=True)
#     description = models.CharField(max_length=255, null=True)
#
#     def __unicode__(self):
#         return self.usergroup.name


class UserPerm(models.Model):
    user = models.ForeignKey(User,verbose_name='用户')
    host = models.ForeignKey(virtualhost,verbose_name='主机')
    timestamp = models.DateTimeField(auto_now=True,verbose_name='授权时间')
    permstatus = models.BooleanField(verbose_name='授权状态',default=False)

    def __unicode__(self):
        return self.user.username + self.host.ip





