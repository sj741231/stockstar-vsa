# -*- coding: utf-8 -*-
__author__ = 'songtao'

import os
from Crypto.PublicKey import RSA
import ssl
from pysphere import VIServer
from vsa.celery import app
from vsa.settings import VCENTER,VCENTERUSER,VCENTERPASSWD

from ansible.inventory import Inventory
from ansible.runner import Runner
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

ssl._create_default_https_context = ssl._create_unverified_context

class esxi():

    def __init__(self,*args,**kwargs):
        self.ip = kwargs.get('vcenter')
        self.user = kwargs.get('user')
        self.passwd = kwargs.get('passwd')
        self.server = VIServer()
        self.server.connect(self.ip,self.user,self.passwd)

    def get_version(self):
        return self.server.get_api_version()

    def getallesxi(self):
        return  self.server.get_hosts()

    def get_esxi_vms(self,host):
        self.server.get_registered_vms()




if __name__ == '__main__':
    a = esxi(**{'vcenter':VCENTER,'user':VCENTERUSER,'passwd':VCENTERPASSWD})
    print a.getallesxi()