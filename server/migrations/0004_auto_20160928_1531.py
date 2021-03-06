# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-28 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_hostgroup_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='hostgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.HostGroup', verbose_name='\u4e3b\u673a\u7ec4'),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.GenericIPAddressField(unique=True, verbose_name='IP\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='host',
            name='name',
            field=models.CharField(help_text='\u4e3b\u673a\u540d-ip\u5730\u5740', max_length=50, unique=True, verbose_name='\u4e3b\u673a\u540d'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='description',
            field=models.CharField(max_length=200, verbose_name='\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='hostgroup',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u4e3b\u673a\u7ec4'),
        ),
    ]
