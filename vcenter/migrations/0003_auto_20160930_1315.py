# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-30 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcenter', '0002_auto_20160930_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualhost',
            name='ip',
            field=models.GenericIPAddressField(null=True, unique=True),
        ),
    ]
