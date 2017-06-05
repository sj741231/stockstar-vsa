# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView,ListView,UpdateView
from django.views.generic.edit import ModelFormMixin, FormMixin, DeleteView, UpdateView
from django.core.urlresolvers import reverse,reverse_lazy
from vsa.genericviews import *
from .models import *
from .forms import *
# Create your views here.



class RecordListView(SuperuserRequiredMixin,ListView):
    model = Records
    template_name = 'recordlist1.html'
    paginate_by = 25

    def get_queryset(self):
        queryset = super(RecordListView,self).get_queryset()
        q = self.request.GET.get("q",None)

        if self.kwargs['zone']:
            queryset = queryset.filter(zone_id=self.kwargs['zone'])
        if q:
            queryset = queryset.filter(host__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RecordListView,self).get_context_data(**kwargs)
        self.zone = self.kwargs.get('zone',None)
        if self.zone:
            context['zone'] = Domain.objects.get(id=self.zone)

        return context


class RecordCreateView(SuperuserRequiredMixin,CreateView):
    # model = Records
    form_class = RecordForm
    template_name = 'records_form.html'
    success_url = reverse_lazy('bind:dnsrecordlist')

    def get_initial(self):
        zone = self.kwargs.get('zone',None)
        if zone:
            self.zone = get_object_or_404(Domain,pk=zone)
            return {'zone':self.zone}

    def get_context_data(self, **kwargs):
        context = super(RecordCreateView, self).get_context_data(**kwargs)
        context['zone'] = self.zone
        context['success_url'] = reverse('bind:dnsrecordlist',kwargs={'zone':self.zone.id})

        return context

    def get_success_url(self):
        return reverse_lazy('bind:dnsrecordlist',kwargs={'zone':self.zone.id})


class RecordUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Records
    form_class = RecordForm
    template_name = 'records_form.html'

    def get_context_data(self, **kwargs):
        context = super(RecordUpdateView,self).get_context_data(**kwargs)
        context['success_url'] = reverse('bind:dnsrecordlist',kwargs={'zone':self.kwargs['zone']})
        return context

    def get_success_url(self):
        return reverse('bind:dnsrecordlist',kwargs={'zone':self.kwargs['zone']})


class RecordDelView(SuperuserRequiredMixin,DeleteView):
    model = Records
    template_name = 'generic/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(RecordDelView,self).get_context_data(**kwargs)
        context['success_url'] = reverse('bind:dnsrecordlist',kwargs={'zone':self.kwargs['zone']})
        return context

    def get_success_url(self):
        return reverse('bind:dnsrecordlist',kwargs={'zone':self.kwargs['zone']})



class RecordView(FormListView):
    template_name = 'recordlist.html'
    model = Records
    # success_url = reverse('bind:dnsrecordlist')
    paginate_by = 25
    form_class = RecordForm

    def get_initial(self):
        initial = super(RecordView,self).get_initial()
        # initial['zone'] = Records.objects.get(zone = self.kwargs['domain'])
        return initial

    def get_context_data(self,**kwargs):
        context = super(RecordView,self).get_context_data(**kwargs)
        context['domain'] = self.kwargs['domain']
        return context

    def get_queryset(self):
        if self.kwargs['domain']:
            self.curren_zone = Domain.objects.get(domain = self.kwargs['domain'])
            qs = self.curren_zone.records_set.all()
        else:
            qs = self.model.objects.all()
        return qs

    def get_success_url(self):
        return reverse('bind:dnsrecordlist')

    # def get_form_kwargs(self,*args,**kwargs):
    #     form_kwargs = super(RecordView,self).get_form_kwargs(**kwargs)
    #     form_kwargs['domain']=self.kwargs['domain']
        # return dict(super(RecordView,self).get_form_kwargs(*args, **kwargs),**{'zone':self.curren_zone})

    # def form_valid(self, form):
    #     form.instance.zone = self.curren_zone
    #     form.save()
    #     return super(RecordView,self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         form = self.form.save(commit=False)
    #         form.zone = self.curren_zone
    #         return HttpResponseRedirect(reverse('bind:dnsrecordlist',kwargs={'domain':self.kwargs['domain']}))
    #     else:
    #         return self.get(request, *args, **kwargs)