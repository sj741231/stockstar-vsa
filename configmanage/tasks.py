# -*- coding: utf-8 -*-


'''
__author__ = 'songtao'
'''



import paramiko
import datetime
import time
import os
from vsa.celery import app
from celery.utils.log import get_task_logger
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()


@app.task(name='backup_switch')
def backup_switch(host,username='cisco',password='7hzi$w!fuP*PB$eP'):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=username,password=password,look_for_keys=False)
    filename = host + '_' +now +'\n'
    c = client.invoke_shell()
    c.send('copy running-config tftp://10.99.12.80\n')
    c.send('\n')
    c.send(filename)
    c.send('\n')
    c.send('\n')
    c.send('\n')
    c.send('\n')
    time.sleep(10)

    c.send('\n')
    print 'backup to server......'
    time.sleep(10)
    c.close()