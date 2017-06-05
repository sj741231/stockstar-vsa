# -*- coding: utf-8 -*-
from __future__ import unicode_literals


__author__ = 'songtao'

from django.forms import ModelForm
from django import forms
from models import *





class NotifyUserForm(ModelForm):
    class Meta:
        model = NotifyUser
        fields = ("username", "telephone","description")
        labels = {
            "username": "用户名",
            "telephone": "电话",
            "description": "描述"
        }
        widgets = {
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "telephone":forms.TextInput(attrs={'class': 'form-control'}),
            "description":forms.Select(attrs={'class':'form-control select2',"style":"width: 100%;"})
        }


class NotifyForm(forms.Form):
    users = forms.ModelMultipleChoiceField(label='用户',queryset=NotifyUser.objects.all(),widget=forms.SelectMultiple(
        attrs={'id':'public-methods'}
    ))
    message = forms.CharField(label='信息内容')
 
 
#edit by shijin     
class NotifyADuserForm(forms.Form):
    aduser = forms.CharField(label='姓名')
    adaccount = forms.CharField(label='账号')
    message = forms.CharField(label='发送信息')
    mobile = forms.CharField(label='手机号', required=False)
    
