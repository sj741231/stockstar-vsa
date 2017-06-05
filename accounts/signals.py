# -*- coding: utf-8 -*-
__author__ = 'songtao'
#



from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver

from tasks import add_user


@receiver(post_save, sender=User)
def mail_to_user(sender, **kwargs):
    print kwargs
    # user = User.objects.get(username=kwargs['username'])
    # print user
    # add_user.delay(user.username, user.email)
