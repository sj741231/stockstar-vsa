#-*-coding=utf8-*-

from __future__ import unicode_literals
__author__ = 'songtao'

from django import forms
from django.forms import ModelForm

# from accounts.models import User,UserGroup
from django.contrib.auth.models import User,Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm


class RegisterForm(forms.Form):
    email = forms.EmailField(label=_(u"邮件"), max_length=30, widget=forms.TextInput(attrs={'size': 30, }))
    password = forms.CharField(label=_(u"密码"), max_length=30, widget=forms.PasswordInput(attrs={'size': 20, }))
    username = forms.CharField(label=_(u"昵称"), max_length=30, widget=forms.TextInput(attrs={'size': 20, }))

    def clean_username(self):
        '''验证重复昵称'''
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"该用户名已经注册"))

    def clean_email(self):
        '''验证重复email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"该邮箱已经被使用请使用其他的"))


class LoginForm(forms.Form):
    username = forms.CharField(label=_(u"用户名"), max_length=30, widget=forms.TextInput(attrs={'size': 20, }),
                               error_messages={'required': u'用户名错误'})
    password = forms.CharField(label=_(u"密码"), max_length=30, widget=forms.PasswordInput(attrs={'size': 20, }),
                               error_messages={'required': u'密码错误'})


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','email')
        labels = {
            'username':u'用户名',
            # 'password':u'密码',
            # 'first_name':u'姓氏',
            # 'last_name':u'名字',
            'email':u'邮件',
            # 'is_superuser':u'超级管理员',
            # 'is_active':u'激活',
        }
        widgets = {
            "username":forms.TextInput(attrs={'class':'form-control'}),
            # "password":forms.TextInput(attrs={'class': 'form-control','type':'password','readonly':'readonly'}),
            # "password":forms.TextInput(attrs={'class': 'form-control','type':'password'}),

            # "first_name":forms.TextInput(attrs={'class': 'form-control'}),
            # "last_name":forms.TextInput(attrs={'class': 'form-control'}),
            "email":forms.TextInput(attrs={'class': 'form-control'}),
            # "is_superuser":forms.CheckboxInput(attrs={'class': 'checkbox'}),
            # "is_active":forms.CheckboxInput(attrs={'class': 'checkbox'})


        }
        help_texts = {
            'email': '@zhengjin99.com'
        }

    # def __init__(self,*args,**kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)

        # self.fields['username'].label = u'用户名'
        # self.fields['first_name'].label = u'姓氏'
        # self.fields['last_name'].label = u'名字'
        # self.fields['email'].label = u'邮件'
        # self.fields['is_staff'].label = u'超级管理员'
        # self.fields['is_active'].label = u'激活'
    # def save(self, commit=True):
    #     user = super(UserForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user



class UserGroupForm(ModelForm):

    users = forms.ModelMultipleChoiceField(
        label='用户',
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            "name" : forms.TextInput(attrs={"class":"form-control"})
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance is not None:
            initial = kwargs.get('initial', {})
            initial['users'] = instance.user_set.all()
            kwargs['initial'] = initial
        super(UserGroupForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super(UserGroupForm, self).save(commit=commit)
        if commit:
            group.user_set = self.cleaned_data['users']
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                group.user_set = self.cleaned_data['users']
            self.save_m2m = new_save_m2m
        return group





class ChangePasswordForm(PasswordChangeForm):

    def __init__(self,user,*args,**kwargs):
        super(ChangePasswordForm,self).__init__(self,*args,**kwargs)
        self.fields['old_password'].widget = forms.TextInput(attrs={'class': 'form-control','type':'password'})
        self.fields['new_password1'].widget = forms.TextInput(attrs={'class': 'form-control','type':'password'})
        self.fields['new_password2'].widget = forms.TextInput(attrs={'class': 'form-control','type':'password'})



