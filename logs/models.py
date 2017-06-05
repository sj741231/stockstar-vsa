from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from vcenter.models import virtualhost

# Create your models here.


class MacRegLog(models.Model):
    authuser = models.CharField(max_length=100)
    checktime = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=200)
    switch = models.CharField(max_length=200)

    class Meta:
        ordering = ['-checktime']

    def __unicode__(self):
        return self.checktime.ctime()+self.mac


class OperatePremissionLog(models.Model):
    opuser = models.ForeignKey(User,related_name='op')
    vsauser = models.ForeignKey(User,related_name='account')
    host = models.ForeignKey(virtualhost)
    timestamp = models.DateTimeField(auto_now=True)


class HostLoginEvent(models.Model):
    user = models.ForeignKey(User)
    host = models.ForeignKey(virtualhost)
    timestamp = models.DateTimeField(auto_now=True)
    log = models.FileField()

    def __unicode__(self):
        return self.user.username + self.host.name


class EsxiScanLog(models.Model):
    timestamp = models.DateField(auto_now=True)
    scanresult = models.IntegerField()
