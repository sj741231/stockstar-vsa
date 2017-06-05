# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-02-04 01:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notifymsg', models.CharField(max_length=60)),
                ('notifytime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotifyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=11)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='notifylog',
            name='notifyuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notify.NotifyUser'),
        ),
    ]
