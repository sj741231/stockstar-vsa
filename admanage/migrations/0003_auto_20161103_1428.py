# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-03 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admanage', '0002_auto_20161101_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adadduserlog',
            name='aduserfile',
            field=models.CharField(max_length=255, verbose_name='\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='groupreleation',
            name='attachto',
            field=models.CharField(blank=True, default=1, max_length=200, verbose_name='\u96b6\u5c5e\u4e8e'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupreleation',
            name='company',
            field=models.CharField(blank=True, default=1, max_length=50, verbose_name='\u516c\u53f8\u540d\u79f0'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupreleation',
            name='department',
            field=models.CharField(blank=True, default=1, max_length=100, verbose_name='\u90e8\u95e8'),
            preserve_default=False,
        ),
    ]
