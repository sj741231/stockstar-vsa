# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''



import json
import urllib2
import sys
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()
from vcenter.models import virtualhost
from django.conf import settings



class zabbix:

    def __init__(self,url=settings.ZABBIX_URL,user=settings.ZABBIX_USER,passwd=settings.ZABBIX_PASSWD):
        self.url = url
        self.user = user
        self.passwd=passwd
        self.header = {"Content-Type": "application/json"}
        self.authID = self.user_login()

    def user_login(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.user,
                    "password": self.passwd
                },
                "id": 0
            })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print "Auth Failed, Please Check Your Name And Password:", e.message
        else:
            response = json.loads(result.read())
            result.close()
            authID = response['result']
            return authID

    def get_data(self, data, hostip=""):
        '''

        :param data: api parm
        :param hostip:
        :return: a dict
        '''
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response

    def host_get(self, hostip):
        '''

        :param hostip:
        :return:
        '''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    # "output": ["hostid", "name", "status", "host"],
                    "output": "extend",
                    "filter": {"host": [hostip]}
                },
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if (res != 0) and (len(res) != 0):
            # for host in res:
            host = res[0]
            if host['status'] == '1':
                return False
            elif host['status'] == '0':
                return host['hostid']
        else:
            # print "Get Host Error or cannot find this host,please check !"
            return False

    def host_del(self,hostip):
        hostid = self.host_get(hostip)
        if hostid == 0:
            print "This host cannot find in zabbix,please check it !"
            # sys.exit()
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.delete",
                "params": [hostid],
                "auth": self.authID,
                "id": 1
            })
        res = self.get_data(data)['result']
        if 'hostids' in res.keys():
            print  "Delet Host:%s success !" % hostip
        else:
            print "Delet Host:%s failure !"  % hostip

    def hostitems_get(self,hostid):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params":{
                    "hostids": hostid,
                    "output": "extend"
                },
                "auth": self.authID,
                "id":1
            }
        )
        result = self.get_data(data)
        return result['result']

    def hostgroup_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                    "output": "extend",
                },
                "auth": self.authID,
                "id": 1,
            })
        res = self.get_data(data)
        if 'result' in res.keys():
            res = res['result']
            if (res != 0) or (len(res) != 0):
                print "Number Of Group: %d " % len(res)
                for host in res:
                    print "HostGroup_id:", host['groupid'], "\t", "HostGroup_Name:", host['name']
                print
        else:
            print "Get HostGroup Error,please check !"

    def template_get(self):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "template.get",
                "params": {
                    "output": "extend",
                },
                "auth": self.authID,
                "id": 1,
            })
        res = self.get_data(data)  # ['result']
        if 'result' in res.keys():
            res = res['result']
            if (res != 0) or (len(res) != 0):
                print "\033[1;32;40m%s\033[0m" % "Number Of Template: ", "\033[1;31;40m%d\033[0m" % len(res)
                for host in res:
                    print "\t", "Template_id:", host['templateid'], "\t", "Template_Name:", host['name']
                print
        else:
            print "Get Template Error,please check !"

    def host_create(self,hostip,groupid,templateid):
        g_list = []
        t_list = []
        for i in groupid.split(','):
            var = {}
            var['groupid'] = i
            g_list.append(var)
        for i in templateid.split(','):
            var = {}
            var['templateid'] = i
            t_list.append(var)
        if hostip and groupid and templateid:
            data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.create",
                    "params": {
                        "host": hostip,
                        "interfaces": [
                            {
                                "type": 1,
                                "main": 1,
                                "useip": 1,
                                "ip": hostip,
                                "dns": "",
                                "port": "10050"
                            }
                        ],
                        "groups": g_list,
                        "templates": t_list,
                    },
                    "auth": self.authID,
                    "id": 1,
                })
            res = self.get_data(data, hostip)
            if 'result' in res.keys():
                res = res['result']
                if 'hostids' in res.keys():
                    print "Create host success"
            else:
                print "Create host failure: %s" % res['error']['data']
        else:
            print  "Enter Error: ip or groupid or tempateid is NULL,please check it !"



if __name__ == "__main__":
    # import os
    # import django
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
    # django.setup()
    from vcenter.models import virtualhost

    hosts = virtualhost.objects.all().filter(updatetime__day='27')
    h1 = []
    for host in hosts:
        if host.ip and 'CentOS' in host.system:
            host_monitor_status = zabbix().host_get(host.ip)
            if not host_monitor_status:
                h1.append(host.ip)


    for h in h1:
        m_39 = zabbix(url='http://172.16.33.39/api_jsonrpc.php',user='tao.song',passwd='St@19871224').host_get(h)
        if not m_39:
            print h