# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-19 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livenode',
            name='address',
            field=models.CharField(max_length=200, verbose_name='\u5730\u5740'),
        ),
    ]