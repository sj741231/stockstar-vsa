# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django.forms import Form,ModelForm
from django import forms
from models import *


class MonitorServerForm(ModelForm):

    class Meta:
        model = MonitorServer

        fields = ("name","url", "user", "password")
        widgets = {
            "name":forms.TextInput(attrs={'class': 'form-control'}),
            "url":forms.TextInput(attrs={'class': 'form-control'}),
            "user":forms.TextInput(attrs={'class': 'form-control'}),
            "password":forms.TextInput(attrs={'class': 'form-control','type':'password'}),
        }

    def __init__(self,*args,**kwargs):
        super(MonitorServerForm,self).__init__(*args,**kwargs)

#
