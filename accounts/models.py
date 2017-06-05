from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

# class UserGroup(models.Model):
#     name = models.CharField(max_length=25,unique=True)
#     descriptions = models.CharField(max_length=100,blank=True)
#
#     def __unicode__(self):
#         return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mobile = models.CharField(max_length=15, blank=True)
    # group = models.ManyToManyField(UserGroup,blank=True)

    def __unicode__(self):
        return self.username
