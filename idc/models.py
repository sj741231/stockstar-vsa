# -*- coding: utf-8 -*-
from django.db import models

from vcenter.models import datacenter

# Create your models here.

class Idc(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'名称')
    tel = models.CharField(max_length=50, verbose_name=u'客服电话')
    address = models.CharField(max_length=200, verbose_name=u'地址')

    def __unicode__(self):
        return self.name


class iptype(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name


# class IpAddress(models.Model):
#     choices = (
#         ('in', u'内网'),
#         ('out', u'外网'),
#         ('pub', u'公网'),
#         ('manager', u'管理地址'),
#     )
#
#     address = models.GenericIPAddressField(verbose_name=u'ip地址')
#     netmask = models.CharField(verbose_name=u'子网掩码', max_length=21)
#     type = models.CharField(choices=choices, verbose_name=u'类型', max_length=50)
#     inuse = models.BooleanField(default=False, verbose_name=u'状态', help_text=u'是否在用')
#     idc = models.ForeignKey(Idc, verbose_name=u'IDC', help_text=u'属于哪个IDC', blank=True, null=True, on_delete=models.SET_NULL)
#
#     def __unicode__(self):
#         return self.address


class Rack(models.Model):
    tag = models.CharField(max_length=40)
    idc = models.ForeignKey(Idc, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.tag



class Racks(models.Model):
    idc = models.ForeignKey(Idc, verbose_name='数据中心')
    pic = models.ImageField(upload_to='static/upload/img', verbose_name='机柜图')
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述')

    def __unicode__(self):
        return self.idc.name +'_'+ self.desc