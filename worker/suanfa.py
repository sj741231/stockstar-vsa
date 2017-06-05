# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''


def maopao(n_list):
    n_len = len(n_list)
    for i in range(n_len):
        print range(1,n_len-i)
        for j in range(1,n_len-i):
            if n_list[j-1] < n_list[j]:
                n_list[j],n_list[j-1] = n_list[j-1],n_list[j]

    return n_list


bb = [999,3,4,6,1,99,2]

cc = maopao(bb)
print cc