# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-06 05:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vcenter', '0013_auto_20161108_1507'),
        ('server', '0004_auto_20160928_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='\u63cf\u8ff0')),
                ('host', models.ManyToManyField(blank=True, to='server.Host', verbose_name='\u4e3b\u673a')),
                ('hostgroup', models.ManyToManyField(blank=True, to='server.HostGroup', verbose_name='\u4e3b\u673a\u7ec4')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
        migrations.CreateModel(
            name='UserPerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='\u6388\u6743\u65f6\u95f4')),
                ('permstatus', models.BooleanField(default=False, verbose_name='\u6388\u6743\u72b6\u6001')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vcenter.virtualhost', verbose_name='\u4e3b\u673a')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
    ]
