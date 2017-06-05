__author__ = 'songtao'
# -*- coding: utf-8 -*-


import sys
import os
import django



# 初始化环境变量
cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from server.models import *
from django.contrib.auth.models import *

userlist = ['test1','test2','test3']

for u in userlist:
    print User.objects.get_or_create(username=u,password=u)

print Group.objects.get_or_create(name='sa')


iplist = ['10.5.6.23','10.5.6.27','10.5.6.35']
for i in iplist:
    print ipaddress.objects.get_or_create(address=i)


print HostGroup.objects.get_or_create(name='operations')
print OperateSystem.objects.get_or_create(name='centos',version='5.5')
print Host.objects.get_or_create(name='test1',ip='10.5.6.23',hostgroup=HostGroup.objects.get(name='operations'),system=OperateSystem.objects.get(name='centos'))
print Host.objects.get_or_create(name='test2',ip='10.5.6.27',hostgroup=HostGroup.objects.get(name='operations'),system=OperateSystem.objects.get(name='centos'))
print Host.objects.get_or_create(name='test3',ip='10.5.6.35',hostgroup=HostGroup.objects.get(name='operations'),system=OperateSystem.objects.get(name='centos'))