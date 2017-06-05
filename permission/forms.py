# -*- coding: utf-8 -*-
__author__ = 'songtao'

from django import forms
from models import *
from tasks import list_user_hosts,add_perm
from vcenter.models import virtualhost


class PermAddForm(forms.ModelForm):

    class Meta:
        model = User_Host
        fields = ("user","host","hostgroup","description",)
        widgets = {
            "user":forms.Select(attrs={'class':'form-control'}),
            "host":forms.SelectMultiple(attrs={'class':'form-control select2',"style":"width: 100%;"}),
            "hostgroup":forms.SelectMultiple(attrs={'class':'form-control select2',"style":"width: 100%;"}),

            "description":forms.TextInput(attrs={'class': 'form-control'}),


        }

    def save(self, commit=True):
        perm = super(PermAddForm, self).save(commit=commit)
        if commit:
            for host in list_user_hosts(perm_id=perm.id):
                add_perm.delay(username=perm.user.username, ip=host)

        return perm



class PermForm(forms.ModelForm):

    class Meta:
        model = User_Host
        fields = ("user","host","hostgroup","description",)
        widgets = {
            "user":forms.Select(attrs={'class':'form-control'}),
            "host":forms.CheckboxSelectMultiple(),
            "hostgroup":forms.CheckboxSelectMultiple(),

            "description":forms.TextInput(attrs={'class': 'form-control'}),


        }


class MuitiAddPerm(forms.Form):
    userlist = forms.ModelMultipleChoiceField(label=u'用户列表',queryset=User.objects.all(),widget=forms.SelectMultiple(
        attrs={'class':'form-control select2',"style":"width: 100%;"}
    ))
    hosts = forms.ModelMultipleChoiceField(label=u'主机列表',queryset=Host.objects.all(),widget=forms.SelectMultiple(
        attrs={'class':'form-control select2',"style":"width: 100%;"}
    ))


class UserPermForm(forms.ModelForm):

    class Meta:
        model = UserPerm
        fields = ("user", "user", "permstatus")
        widgets = {
            "user":forms.Select(attrs={'class': 'form-control','disabled':'disabled'}),
            "host":forms.TextInput(attrs={'class': 'form-control'}),
            "permstatus":forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(UserPermForm,self).__init__(*args,**kwargs)



class UserPermform1(forms.Form):
    userlist = forms.ModelMultipleChoiceField(label=u'用户列表',queryset=User.objects.all(),widget=forms.SelectMultiple(
        attrs={'class':'form-control select2',"style":"width: 100%;"}
    ))
    hosts = forms.ModelMultipleChoiceField(label=u'主机列表',queryset=virtualhost.objects.all(),widget=forms.SelectMultiple(
        attrs={'class':'form-control select2',"style":"width: 100%;"}
    ))