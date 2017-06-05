#-*-coding=utf8-*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.



class quicklink(models.Model):
    name = models.CharField(verbose_name=u'名称',max_length=255)
    link = models.URLField(verbose_name=u'链接')