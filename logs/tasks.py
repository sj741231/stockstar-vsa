# -*- coding: utf-8 -*-
__author__ = 'songtao'


import os
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

from django.core.mail import EmailMultiAlternatives,EmailMessage
from vsa.celery import app
from celery.utils.log import get_task_logger
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from .models import *

import datetime


@app.task(name="collect_ip_mac")
def walk_core_switch(timeout=30):
    s = cmdgen.CommandGenerator()
    print datetime.datetime.now()
    errorIndication,errorStatus,errorIndex,varBinds = s.nextCmd(
        cmdgen.CommunityData('zhengjin99.com'),
        cmdgen.UdpTransportTarget(('172.16.39.1',161),timeout=timeout,retries=0),
        '1.3.6.1.2.1.3.1.1.2',
        maxRows = 5000,

    )
    print datetime.datetime.now()
    if errorIndication:
        print errorIndication
    elif errorStatus:
        print errorStatus.prettyPrint()
    else:
        for row in varBinds:
            for key,val in row:
                ip = key.prettyPrint().split('.')[-4:]
                mac = val.prettyPrint()[2:]
                detail = {'ip':'.'.join(ip),'mac':mac}
                MacRegLog.objects.create(**detail)
        return 'ok'