# -*- coding: utf-8 -*-
from __future__ import unicode_literals



from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Domain(models.Model):
    domain = models.CharField(max_length=255,verbose_name='域名')

    def __unicode__(self):
        return self.domain

    def get_absolute_url(self):
        return reverse('bind:dnsrecordlist')


class Records(models.Model):
    choice = (
        ('A', 'A'),
        ('CHAME', 'CHAME'),
        ('MX', 'MX'),
        ('NS', 'NS'),
        ('PTR', 'PTR'),
        ('SOA', 'SOA'),
    )
    status_cat = (
        ('online', '在线'),
        ('offline', '离线'),
    )
    zone = models.ForeignKey(Domain)
    host = models.CharField(max_length=255, verbose_name='主机记录',blank=True)
    type = models.CharField(max_length=20, choices=choice, default='A', verbose_name='记录类型')
    data = models.TextField(max_length=255, blank=True, verbose_name='记录值')
    ttl = models.IntegerField(default=600)
    mx_priority = models.IntegerField(null=True, verbose_name='MX优先级')
    refresh = models.IntegerField(default=3600)
    retry = models.IntegerField(default=3600)
    expire = models.IntegerField(default=600)
    minimum = models.IntegerField(default=3600)
    serial = models.BigIntegerField(default=20161107)
    resp_person = models.CharField(max_length=255, blank=True)
    primary_ns = models.CharField(max_length=255, blank=True)
    status = models.CharField(choices=status_cat, default='online', max_length=10)

    def __unicode__(self):
        return self.host + '.' + self.zone.domain


class xfr(models.Model):
    zone = models.CharField(max_length=255)
    client = models.CharField(max_length=255)




