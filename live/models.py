# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
# Create your models here.



class video(models.Model):
    type_cat = (
        ('rtmp', 'rtmp'),
        ('hls', 'hls'),
    )

    name = models.CharField(max_length=255,verbose_name='名称')
    stream_type = models.CharField(choices=type_cat,verbose_name='类型',max_length=10)
    address = models.CharField(max_length=100,verbose_name='地址')


class LiveChannel(models.Model):
    name = models.CharField(max_length=255,verbose_name='频道名称')

    def __unicode__(self):
        return self.name


class LiveNode(models.Model):
    pro_cat = (
        ('rtmp','rtmp'),
        ('http','http')
    )
    name = models.CharField(max_length=50,verbose_name='名称')
    channal = models.ForeignKey(LiveChannel,verbose_name='频道')
    protocol = models.CharField(max_length=10,verbose_name='协议',choices=pro_cat)
    address = models.CharField(verbose_name='地址',max_length=200)

    def __unicode__(self):
        return  self.name

