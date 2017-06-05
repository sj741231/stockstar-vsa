# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-24 05:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostgroup',
            name='manager',
        ),
        migrations.AlterField(
            model_name='host',
            name='hostgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.HostGroup'),
        ),
    ]