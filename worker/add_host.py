# -*- coding: utf-8 -*-
__author__ = 'songtao'


import os
import sys
import django

cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from server.models import *


f = open('/root/hostlist')

for i in f.readlines():
    ip = i.strip('\n')
    hostname = ip.split('.')[-2:]
    hostname = 'db-' + '-'.join(hostname)
    print Host.objects.get_or_create(name=hostname,ip=ip)
