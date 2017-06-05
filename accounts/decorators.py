# -*- coding: utf-8 -*-
__author__ = 'songtao'


from django.http.response import HttpResponseRedirect


def admin_required(func):
    """要求用户是admin的装饰器"""
    def _deco(request, *args, **kwargs):
        if not request.session.get('admin'):
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)
    return _deco
