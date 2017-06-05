# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django import forms
from .models import MacRegLog



class MacRegLogForm(forms.ModelForm):

    class Meta:
        model = MacRegLog
        fields = ("authuser","ip","mac","switch",)