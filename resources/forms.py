# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''

from django import forms
from .models import IpAddress



class IpAddressForm(forms.ModelForm):
    class Meta:
        model = IpAddress
        fields = ['address','inuse']
        widgets = {
            "address":forms.TextInput(attrs={'class': 'form-control'})


        }