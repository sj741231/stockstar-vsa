# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from resources.models import IpAddress

# Create your models here.




class NetworkEquipment(models.Model):
    name = models.CharField(max_length=50, unique=True,error_messages={'unique':'设备已经存在'},verbose_name='名称')
    ip = models.ForeignKey(IpAddress,verbose_name='IP地址')
    vender = models.CharField(max_length=20,verbose_name='厂商')
    model = models.CharField(max_length=25,verbose_name='型号')
    sn = models.CharField(max_length=25, null=True, blank=True,verbose_name='编号')
    asset_tag = models.CharField(max_length=25, null=True, blank=True,verbose_name='资产标签')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name




class Switch(NetworkEquipment):
    def get_absolute_url(self):
        return reverse('assets:switchlist')


#
from django.db.models.signals import pre_save,post_save,pre_delete
from django.dispatch import receiver




@receiver(pre_delete,sender = Switch)
def equipment_ip_recycle(sender,**kwargs):
    device = kwargs['instance']
    if device.ip.address:
        IpAddress.objects.filter(address=device.ip.address).update(inuse=False)



@receiver(pre_save,sender = Switch)
def equipment_ip_use(sender,**kwargs):
    device = kwargs['instance']
    if device.ip.address:
        IpAddress.objects.filter(address=device.ip.address).update(inuse=True)