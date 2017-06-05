# -*- coding: utf-8 -*-

from django.shortcuts import render,get_object_or_404

from django.http.response import HttpResponse
# Create your views here.

from .tasks import backup_switch
from assets.models import Switch


def backup_view(request,pk):
    switch = get_object_or_404(Switch,pk=int(pk))
    if switch.ip.address:
        backup_switch.delay(switch.ip.address)
        return HttpResponse("<script> alert('" + u'备份中!' + "');window.location.href='/assets/switchback'</script>")