# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-13 01:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('idc', '0006_auto_20170204_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipaddress',
            name='idc',
        ),
        migrations.DeleteModel(
            name='Ipaddress',
        ),
    ]
