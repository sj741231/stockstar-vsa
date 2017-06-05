# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-29 08:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='datacenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u79f0')),
                ('cpu', models.CharField(max_length=50)),
                ('memory', models.CharField(max_length=50)),
                ('disk', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('servercontainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vcenter.datacenter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='vm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u540d\u79f0')),
                ('cpu', models.CharField(max_length=50, null=True)),
                ('memory', models.CharField(max_length=50, null=True)),
                ('disk', models.CharField(max_length=50, null=True)),
                ('ip', models.GenericIPAddressField(unique=True)),
                ('esxi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vcenter.host')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]