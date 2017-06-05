# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-01 03:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vcenter', '0011_auto_20161010_1742'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logs', '0003_operatepremissionlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostLoginEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('log', models.FileField(upload_to=b'')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vcenter.virtualhost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]