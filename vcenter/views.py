# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import ListView,DetailView,View,TemplateView
from django.http.response import HttpResponse
from django.utils import timezone
import arrow
from .models import datacenter,host,virtualhost
import json
from vsa.genericviews import LoginRequiredMixin

# Create your views here.

def leftlist(request):
    data = [{'name':x.name,'id':x.id,'vmcount':sum([y.virtualhost_set.all().count() for y in x.host_set.all()])} for x in datacenter.objects.all()]
    # print data
    return HttpResponse(json.dumps(data))


class DatacenterListView(LoginRequiredMixin,DetailView):
    model = datacenter
    template_name = 'datacentervmlist.html'

    def get_queryset(self):
        qs = super(DatacenterListView, self).get_queryset()
        return qs.filter(id=self.kwargs['pk'])




class VcenterDetail(LoginRequiredMixin,TemplateView):

    template_name = 'datacenterindex.html'

    def get_context_data(self, **kwargs):
        context = super(VcenterDetail, self).get_context_data(**kwargs)
        context['clusters'] = datacenter.objects.all()
        context['hosts'] = host.objects.all()
        context['vms'] = virtualhost.objects.all()
        self.get_vm_updatecount()
        context['time_line'] = self.time_line
        context['vm_count_by_time'] = self.vm_count_by_time
        return context

    def get_vm_updatecount(self):
        now = arrow.now()
        self.time_line = []
        self.vm_count_by_time = []
        for i in range(0,30):
            date = now.replace(days=-i)
            self.time_line.append(date.strftime('%Y-%m-%d'))
            count1 = virtualhost.objects.filter(updatetime__range=(date.floor('day').datetime,date.ceil('day').datetime)).count()
            # yield [date.strftime('%Y-%m-%d'),virtualhost.objects.filter(timestamp__range=(date.floor('day').datetime,date.ceil('day').datetime)).count()]
            self.vm_count_by_time.append(count1)