# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''

from .models import IpAddress


def update_ip_use_status(ip, inuse):
    IpAddress.objects.filter(address=ip).update(inuse=inuse)