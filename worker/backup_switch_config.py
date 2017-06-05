# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''

import paramiko
import datetime
import time
import sys


def backup_switch(host,user,passwd):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=user,password=passwd)
    filename = host + '_' +now +'\n'
    c = client.invoke_shell()
    c.send('copy running-config tftp://10.99.12.80:69 \n')
    c.send(filename)
    # print c.recv(1024)
    c.send('\n')
    c.send('\n')
    c.send('\n')
    c.send('\n')
    c.send('\n')
    print 'backup to server......'
    time.sleep(5)

    client.close()

if __name__ == '__main__':
    backup_switch(host='10.99.12.1',user='cisco',passwd='ejpSy3vxy3oHZ4pIox74')