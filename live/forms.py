# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django import forms
from .models import *


class VideoForm(forms.ModelForm):
    class Meta:
        model = video
        fields = ['name','stream_type','address']
        widgets = {
            "name":forms.TextInput(attrs={'class': 'form-control'}),
            "stream_type":forms.Select(attrs={'class': 'form-control'}),
            "address":forms.TextInput(attrs={'class': 'form-control'})

        }

class LiveChannelForm(forms.ModelForm):
    class Meta:
        model = LiveChannel
        fields = ['name']
        widgets = {
            "name":forms.TextInput(attrs={'class': 'form-control'}),

        }


class LiveNodeForm(forms.ModelForm):
    class Meta:
        model = LiveNode
        fields = ['name','channal','protocol','address']
        widgets = {
            "name":forms.TextInput(attrs={'class': 'form-control'}),
            "channal":forms.Select(attrs={'class': 'form-control'}),
            "protocol":forms.Select(attrs={'class': 'form-control'}),
            "address":forms.TextInput(attrs={'class': 'form-control'}),

        }