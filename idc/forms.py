# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django.forms import ModelForm
from django import forms
from models import *


class IdcForm(ModelForm):
    class Meta:
        model = Idc
        fields = ("name", "tel", "address")
        widgets = {
            "name":forms.TextInput(attrs={'class':'form-control'}),
            "tel":forms.TextInput(attrs={'class': 'form-control'}),
            "address":forms.TextInput(attrs={'class': 'form-control'})

        }

    def __init__(self, *args, **kwargs):
        super(IdcForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = u"名称"
        self.fields["tel"].label = u"联系电话"
        self.fields["address"].label = u"地址"


class RackForm(ModelForm):
    class Meta:
        model = Rack
        fields = ("tag", "idc")
        labels = {
            "tag": u"机柜标签",
            "idc": u"idc机房"
        }
        widgets = {
            "tag":forms.TextInput(attrs={'class':'form-control'}),
            "idc":forms.Select(attrs={'class': 'form-control'})

        }


# class IpForm(ModelForm):
#     class Meta:
#         model = IpAddress
#         fields = ("address", "type", "inuse", "idc")
#         widgets = {
#             "address":forms.TextInput(attrs={'class':'form-control'}),
#             "type":forms.Select(attrs={'class':'form-control'}),
#             # "status":forms.RadioChoiceInput(attrs={'class':'form-control'}),
#             "idc":forms.TextInput(attrs={'class': 'form-control'})
#
#         }


class RacksForm(forms.ModelForm):
    class Meta:
        model = Racks
        fields = ("idc","pic","desc")
        widgets = {
            "idc":forms.Select(attrs={'class':'form-control'}),
            # "pic":forms.Select(attrs={'class':'form-control'}),
            "desc":forms.TextInput(attrs={'class': 'form-control'})

        }