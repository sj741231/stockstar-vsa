# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django import forms
from models import *


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ("name", "ip", "hostgroup")
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "ip": forms.TextInput(attrs={'class': 'form-control'}),
            "hostgroup": forms.Select(attrs={'class': 'form-control select2', "style": "width: 100%;"}),

            # "":forms.Select(attrs={'class':'form-control'}),
            # "status":forms.RadioChoiceInput(attrs={'class':'form-control'}),
            # "idc":forms.Select(attrs={'class': 'form-control'}
        }


class HostGroupForm(forms.ModelForm):
    host = forms.ModelMultipleChoiceField(queryset=Host.objects.filter(hostgroup__isnull=True), label=u'主机',
                                          widget=forms.SelectMultiple(attrs={'class': 'form-control select2',"style": "width: 100%;"}))

    class Meta:
        model = HostGroup
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.TextInput(attrs={'class': 'form-control'})

        }

    def __init__(self, *args, **kwargs):
        super(HostGroupForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(HostGroupForm, self).save(commit=commit)
        if commit:
            hosts = self.cleaned_data['host']
            group.host_set = hosts
            # for host in hosts:
            #     host.hostgroup = group
            #     host.save()
        return group


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("user", "host", "log")
