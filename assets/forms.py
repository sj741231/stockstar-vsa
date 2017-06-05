# -*- coding: utf-8 -*-

from __future__ import unicode_literals

'''
__author__ = 'songtao'
'''

from django import forms
from .models import NetworkEquipment,Switch


class NetworkEquipmentForm(forms.ModelForm):
    class Meta:
        model = NetworkEquipment
        fields = ('name','ip','vender','model','sn','asset_tag',)



class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = ('name','ip','vender','model','sn','asset_tag',)
        widgets = {
            "ip":forms.Select(attrs={'class': 'form-control'}),
            "name":forms.TextInput(attrs={'class': 'form-control'}),
            "vender":forms.TextInput(attrs={'class': 'form-control'}),
            "model":forms.TextInput(attrs={'class': 'form-control'}),
            "sn":forms.TextInput(attrs={'class':'form-control'}),
            "asset_tag":forms.TextInput(attrs={'class':'form-control'}),

        }