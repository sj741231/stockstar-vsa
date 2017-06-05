# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models


# Create your models here.


class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class datacenter(BaseModel):
    pass


class host(BaseModel):
    cpu = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    disk = models.CharField(max_length=255)
    ip = models.GenericIPAddressField(null=True)
    esxi_groups = models.ForeignKey(datacenter, on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('vcenter:serverdetail', args=[str(self.id)])


class virtualhost(BaseModel):
    vmuuid = models.CharField(max_length=255)
    cpu = models.CharField(max_length=255, null=True)
    memory = models.CharField(max_length=50, null=True)
    disk = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField(null=True)
    system = models.CharField(max_length=100, verbose_name='操作系统', null=True)
    esxi = models.ForeignKey(host, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.CharField(max_length=255, verbose_name="标签", null=True)
    updatetime = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('vcenter:vmdetail', args=[str(self.id)])



