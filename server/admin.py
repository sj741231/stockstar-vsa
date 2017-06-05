from django.contrib import admin
from django.forms import ModelForm
from django.db.models import Q

from server.models import *

# Register your models here.



# class HostAdminForm(ModelForm):
#
#     class Meta :
#         model = Host
#
#     def __init__(self):
#         super(HostAdminForm,self).__init__(*args, **kwargs)
#         if self.instance.id:
#             if self.instance.ip_id:
#                 ip_list = ipaddress.objects.filter(
#                     Q(id=self.instance.ip_id) |
#                     Q(inuse=False)
#                 )
#                 ip_field = self.field



# class IpAdmin(admin.ModelAdmin):
#     list_display = ('address',)


class OperateAdmin(admin.ModelAdmin):
    list_display = ('name','version',)


class HostGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # filter_horizontal = ('manager',)
    search_fields = ['name','manager']



class HostAdmin(admin.ModelAdmin):
    list_display = ['name','ip','hostgroup']
    # filter_horizontal = ('manager',)
    search_fields = ['name','ip']


class EventAdmin(admin.ModelAdmin):
    list_display = ('user','host','timestamp','log',)



# admin.site.register(ipaddress,IpAdmin)
admin.site.register(HostGroup,HostGroupAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(Event,EventAdmin)