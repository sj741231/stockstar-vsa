# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-21 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bind', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='host',
            field=models.CharField(blank=True, max_length=255, verbose_name='\u4e3b\u673a\u8bb0\u5f55'),
        ),
    ]
