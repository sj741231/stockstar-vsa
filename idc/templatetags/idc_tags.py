# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django import template

register = template.Library()


def get_field_verbose_name(instance):
    #django 1.7 中获取field verbors_name
    return instance._meta.fields



def get_queryset_field_verbose_name(queryset, arg):
    return queryset.model._meta.get_field(arg).verbose_name



register.filter('field_verbose_name', get_field_verbose_name)
register.filter('queryset_field_verbose_name', get_queryset_field_verbose_name)
