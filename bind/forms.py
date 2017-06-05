# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django.forms import Form,ModelForm
from django import forms
from models import *


class RecordForm(ModelForm):

    class Meta:
        model = Records

        fields = ("zone","host", "type", "data", "ttl", "primary_ns")
        widgets = {
            "zone":forms.Select(attrs={'class': 'form-control','disabled':'disabled'}),
            "host":forms.TextInput(attrs={'class': 'form-control'}),
            "type":forms.Select(attrs={'class': 'form-control'}),
            "data":forms.TextInput(attrs={'class': 'form-control'}),
            "ttl":forms.TextInput(attrs={'class': 'form-control'}),
            "primary_ns":forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        # self.zone = kwargs.pop('zone',None)
        # self.fileds['zone'].initial = self.zone
        super(RecordForm,self).__init__(*args,**kwargs)

#

class DomainForm(ModelForm):
    class Meta:
        model = Domain
        fields = ("domain",)
        widgets = {
            "domain":forms.TextInput(attrs={'class': 'form-control'})
        }
