__author__ = 'songtao'
# -*- coding: utf-8 -*-

f = open('ip.list','r')
msg = ''
for i in f.readlines():
   msg += 'usr/' + i.split(' ')[2].replace('\n',' ')
f.close()
print msg