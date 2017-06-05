# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django  import forms

from models import *



class LinkForm(forms.ModelForm):

    class Meta:
        model = quicklink
        fields = ("name","link")
        widgets = {
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "link":forms.TextInput(attrs={'class': 'form-control'}),
        }

