# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.




class NotifyUser(models.Model):
    username = models.CharField(max_length=255)
    telephone = models.CharField(max_length=11)
    description = models.CharField(max_length=255,blank=True)

    def __unicode__(self):
        return self.username


class NotifyLog(models.Model):
    notifymsg = models.CharField(max_length=60)
    notifytime = models.DateTimeField(auto_now=True)
    notifyusers = models.TextField(verbose_name='被通知用户')
    detail = models.TextField(verbose_name='通知详情')

    def __unicode__(self):
        return self.notifymsg