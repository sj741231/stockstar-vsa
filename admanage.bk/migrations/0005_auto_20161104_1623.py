# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-04 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admanage', '0004_auto_20161104_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='adadduserlog',
            name='addaduserstatus',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adadduserlog',
            name='detail',
            field=models.TextField(blank=True),
        ),
    ]