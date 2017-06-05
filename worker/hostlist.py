# -*- coding: utf-8 -*-
import os
import sys
import django
import xlrd

cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from server.models import *
import json
import argparse

#f = xlrd.open_workbook('/root/vm-all02.xlsx')
#table = f.sheet_by_name("Sheet1")
#rows = table.nrows
#for i in range(1,rows):
#    row_value = table.row_values(i)
#    try:
#        print Host.objects.get_or_create(name=row_value[0],ip=row_value[2])
#    except:
#        pass

#f = open('/root/hostlist')
#
#for i in f.readlines():
#    ip = i.strip('\n')
#    
#    hostname = ip.split('.')[-2:]
#    hostname = 'db-' + '-'.join(hostname)
#    print Host.objects.get_or_create(name=hostname,ip=ip)
class DjangoInventory(object):
    def __init__(self):
        self.conn = None

        self.inventory = dict()  # A list of groups and the hosts in that group
        self.cache = dict()  # Details about hosts in the inventory

        # Read settings and parse CLI arguments
        # self.read_settings()
        self.parse_cli_args()

        # Cache
        if self.args.refresh_cache:
            pass
        else:
            pass

        data_to_print = ""

        if self.args.host:
            data_to_print = self.djangohost()

        elif self.args.list:
            # Display list of instances for inventory
            data_to_print = self.djangohost()

        else:  # default action with no options
            pass

        print data_to_print

    def djangohost(self):
        """
    
        """
        hostlists = []
        hosts = Host.objects.all().values_list('name','ip')
        for i,k in hosts:
            #hostlists.append(str(k))
            print str(k)
#        print json.dumps(hostlists)
        return json.dumps(hostlists)

    def parse_cli_args(self):
        """ Command line argument processing """
    
        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on Cobbler')
        parser.add_argument('--list', action='store_true', default=True, help='List instances (default: True)')
        parser.add_argument('--host', action='store', help='Get all the variables about a specific instance')
        parser.add_argument('--refresh-cache', action='store_true', default=False,
                            help='Force refresh of cache by making API requests to cobbler (default: False - use cache files)')
        self.args = parser.parse_args()



DjangoInventory()
