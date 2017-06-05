from django.contrib import admin
from django.forms import ModelForm
from django.db.models import Q
from permission.models import *
from server.models import *
# Register your models here.


class UserHostAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_display = ['user']
    fields = ('user','host','hostgroup')
    filter_horizontal = ('host','hostgroup')


# class UserGroupHostAdmin(admin.ModelAdmin):
#     search_fields = ('usergroup__name',)
#     fields = ['usergroup','host','hostgroup']
#     filter_horizontal = ['host','hostgroup']



admin.site.register(User_Host,UserHostAdmin)
# admin.site.register(Usergroup_Hostgroup,UserGroupHostAdmin)