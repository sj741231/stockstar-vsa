# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-01 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admanage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupreleation',
            name='attachto',
            field=models.CharField(max_length=200, null=True, verbose_name='\u96b6\u5c5e\u4e8e'),
        ),
        migrations.AlterField(
            model_name='groupreleation',
            name='company',
            field=models.CharField(max_length=50, null=True, verbose_name='\u516c\u53f8\u540d\u79f0'),
        ),
    ]