# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from shortcuts import md5Checksum
# Create your models here.


class IpAddress(models.Model):
    address = models.GenericIPAddressField(verbose_name='IP地址')
    inuse = models.BooleanField(default=False, verbose_name='状态', help_text='是否在用')

    def __unicode__(self):
        return self.address


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    deploy_path = models.CharField(max_length=255,  blank=True)
    backup_path = models.CharField(max_length=255,  blank=True)
    service_stop_command = models.CharField(max_length=255,  blank=True)
    service_start_command = models.CharField(max_length=255,  blank=True)
    description = models.CharField(max_length=255,  blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class BaseFileObject(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100,  blank=True)
    upload_time = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User)
    md5 = models.CharField(max_length=50)
    md5_auto = models.CharField(max_length=50)

    class Meta:
        abstract = True
        ordering = ('-upload_time',)

    def __unicode__(self):
        return self.name


class Script(BaseFileObject):
    project = models.OneToOneField(Project, null=True, blank=True)
    file = models.FileField(
        upload_to='upload/script/%Y/%m/%d/%H/%M/%S/'

    )

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.name


class CommonFile(BaseFileObject):
    file = models.FileField(
        upload_to='upload/commonfile/%Y/%m/%d/%H/%M/%S/'

    )

    def __unicode__(self):
        return self.name


def update_md5(sender, **kwargs):
    obj = kwargs['instance']
    if not obj.md5_auto:
        filepath = obj.file.path
        md5sum = md5Checksum(filepath)
        sender.objects.filter(pk=obj.pk).update(md5_auto=md5sum)


class Package(BaseFileObject):
    file = models.FileField(
        max_length=2048,
        upload_to='upload/mypackage/%Y/%m/%d/%H/%M/%S/'

    )
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)
    create_release_list = models.BooleanField(default=0)

    def __unicode__(self):
        return self.name


post_save.connect(update_md5, sender=CommonFile)
post_save.connect(update_md5, sender=Script)
post_save.connect(update_md5, sender=Package)