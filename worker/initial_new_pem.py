# -*- coding: utf-8 -*-

from __future__ import unicode_literals
__author__ = 'songtao'

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

from django.contrib.auth.models import *
from server.models import *
from permission.models import *
from vcenter.models import *



perms = User_Host.objects.all()

for p in perms:
    for h in p.host.all():
        print p.user, h.ip
        host = virtualhost.objects.filter(ip=h.ip)
        if EsxiHost:
            host = virtualhost.objects.get(ip=h.ip)
            UserPerm.objects.get_or_create(**{'user':p.user,'host':EsxiHost})
        else:
            print '主机:%s  不存在' % h.ip
        # if not UserPerm.objects.filter(host=host):
        #     UserPerm.objects.create(**{'user':p.user,'host':host})
