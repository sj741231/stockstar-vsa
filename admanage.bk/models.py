# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.


class GroupReleation(models.Model):
    adtree = models.CharField(max_length=100,verbose_name=u'ad目录树')
    department = models.CharField(max_length=100,blank=True,verbose_name=u'部门',)
    attachto = models.CharField(max_length=200,verbose_name=u'隶属于',blank=True)
    company = models.CharField(max_length=50,verbose_name=u'公司名称',blank=True)

    def __unicode__(self):
        return self.adtree


class AdUserfile(models.Model):
    xls_file = models.FileField(upload_to='upload/xls/%Y/%m/%d/%H/%M')
    uploadtime = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User)

    def __unicode__(self):
        return self.xls_file.name


class AdAddUserLog(models.Model):
    aduser = models.CharField(max_length=50,verbose_name='ad用户名',blank=True)
    adaccount = models.CharField(max_length=255,verbose_name='邮件地址',blank=True)
    department = models.CharField(max_length=255,verbose_name='部门',blank=True)
    vlangroup = models.CharField(max_length=255,blank=True)
    addaduserstatus = models.BooleanField()
    aduserfile = models.CharField(max_length=255,verbose_name=u'文件')
    timestamp = models.DateTimeField(auto_now=True, verbose_name=u'添加时间')
    detail = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('admanage:adlogdetail', args=[str(self.id)])

    class Meta:
        ordering = ['-id']