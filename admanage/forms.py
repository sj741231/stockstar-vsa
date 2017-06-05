# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'songtao'

import xlrd
from django import forms
from .models import *



class AduserFileForm(forms.ModelForm):
    class Meta:
        model = AdUserfile
        fields = ("xls_file",)
        # widgets = {
        #     "uploader":forms.FileField(attrs={'class': 'form-control'}),
        # }

    # def __init__(self,*args,**kwargs):
    #     self.uploader = kwargs.pop('uploder',none)
    #     self.fields['uploader'].initial = self.uploader.id
    #     super(AduserFileForm, self).__init__(*args,**kwargs)

class GroupReleationForm(forms.ModelForm):
    class Meta:
        model = GroupReleation
        fields = ("department","attachto","adtree","company")
        widgets = {
            "adtree" : forms.TextInput(attrs={"class":"form-control"}),
            "department" : forms.TextInput(attrs={"class":"form-control"}),
            "attachto" : forms.TextInput(attrs={"class":"form-control"}),
            "company" : forms.TextInput(attrs={"class":"form-control"})

        }
        labels = {
            'adtree':'ad目录',
            'department':'部门',
            'attachto':'属组',
            'company':'公司'

        }


class ImportGroupRelationXls(forms.Form):
    xlsfile = forms.FileField(label='文件')