# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-10 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcenter', '0009_virtualhost_updatetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualhost',
            name='vmuuid',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
