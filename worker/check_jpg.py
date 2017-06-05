# -*- coding: utf-8 -*-
__author__ = 'songtao'

import os
import sys
import urllib2
import requests
import datetime

timelist = ['0920', '1000', '1300', '1350', '1430', '1530', '1700', '1900']

hosts = ["10.100.10.123", "10.100.10.124", "10.101.10.123", "10.101.10.124", "172.16.33.247", "172.16.33.114"]

now_date = datetime.date.today().strftime('%Y%m%d')

# url = "http://vd.jrj.com/front/video/index.jsp?id=Colu1438680606583144"
#
# html_doc = urllib2.urlopen(url).read()
# data=requests.get(url)
#
# print data.status_code
# print now_date



for host in hosts:
    url = 'http://%s/zjwlyx/%s.jpg' % (host, 201607111000)
    status = requests.get(url).status_code
    print type(status)
    if status != 200:
        print "%s----%s" % (host, status)

    else:
        print "warning:%s---%s" %(host,status)
