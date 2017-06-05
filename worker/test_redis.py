# -*- coding: utf-8 -*-
__author__ = 'songtao'
import time
from rediscluster import StrictRedisCluster

cluster = [{'host': '10.99.12.109', 'port': 7000}, {'host': '10.99.12.109', 'port': 7001},
           {'host': '10.99.12.109', 'port': 7002}, {'host': '10.99.12.110', 'port': 7000},
           {'host': '10.99.12.110', 'port': 7001}, {'host': '10.99.12.110', 'port': 7002}]

r = StrictRedisCluster(startup_nodes=cluster, decode_responses=True)

print time.ctime()

for i in range(10000):
    key = 'test_key_%s' %i
    r.append(key,i)

t2= time.localtime()

print time.ctime()