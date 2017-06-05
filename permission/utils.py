# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django.contrib.auth.models import User,Group



class UserPerms(object):

    def __init__(self,username):
        self.username = username
        try:
            self.user = User.objects.get(username=self.username)
        except:
            print 'user not exists'

