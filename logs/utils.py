# -*- coding: utf-8 -*-
__author__ = 'songtao'


# from pysnmp.hlapi.asyncore import *
#
import os
from pysnmp.entity.rfc3413.oneliner import cmdgen
import django
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from logs.models import *

# s = cmdgen.CommandGenerator()

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
    varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
        return 1
    if errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1] or '?')                                                                                      )
        return 1
    for row in varBinds:
        for oid,val in row:
            ip = oid.prettyPrint().split('.')[-4:]
            mac = val.prettyPrint()[2:]
            detail = {'ip':'.'.join(ip),'mac':mac}
            MacRegLog.objects.create(**detail)
            # print detail
        # if val is None:
        #     print(oid.prettyPrint())
        # else:
        #     print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

import datetime

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

                # print detail


def use_snmpwalk():
    result = os.popen('snmpwalk -v 2c -c zhengjin99.com 172.16.39.1 .1.3.6.1.2.1.3.1.1.2').read().split('\n')[:-1]
    # print result
    for i in result:
        # print i.split('=')
        k,v = i.split('=')
        ip = '.'.join(k.split('.')[-4:])
        mac = ''.join(v.split(':')[-1].split())
        detail = {'ip':ip,'mac':mac.lower()}
        MacRegLog.objects.create(**detail)


if __name__ == '__main__':
    # walk_core_switch(300)
    # cmdGen = cmdgen.AsynCommandGenerator()
    # cmdGen.nextCmd(
    #     cmdgen.CommunityData('zhengjin99.com'),
    #     cmdgen.UdpTransportTarget(('172.16.39.1',161),timeout=5,retries=0),
    #     ('1.3.6.1.2.1.3.1.1.2',),
    #     (cbFun, None)
    # )
    # cmdGen.snmpEngine.transportDispatcher.runDispatcher()
    use_snmpwalk()