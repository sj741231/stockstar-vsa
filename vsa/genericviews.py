# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'songtao'

from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin, FormMixin, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.http import Http404, HttpResponseRedirect,HttpResponseNotAllowed,HttpResponseForbidden
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.views import redirect_to_login, logout_then_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import (HttpResponseRedirect, HttpResponsePermanentRedirect,
                         Http404, HttpResponse)
from django.shortcuts import resolve_url
from django.utils.encoding import force_text
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin




from functools import wraps

def requires_permission(f):
    @wraps(f)
    def decorated(request,*args, **kwargs):
        user_perm = [x for x in request.user.userurlpermission_set.all()]
        user_group = [g for g in request.user.usergroup_set.all()]
        for i in user_group:
            i.usergroupurlpermission_set.all()
        return f(*args, **kwargs)
    return decorated





def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


class SuperuserRequiredMixin(object):
    """
    Mixin allows you to require a user with `is_superuser` set to True.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            # return HttpResponseForbidden()
            return HttpResponse("<script> alert('" + '操作不允许，请联系管理员:' + "');window.location.href='/'</script>")

        return super(SuperuserRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class UserPermissionMixin(object):

    def dispatch(self,request,*args,**kwargs):
        if request.url in request.user.rollbackmainjob_set:
            return HttpResponse("<script> alert('" + u'任务未发布，无法回退:' + "');window.location.href='/deploy/rollback'</script>")



# @class_view_decorator(login_required)
class FormListView(ModelFormMixin, SuperuserRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 定义post方法，保存form数据,返回成功列表页
        # self.object = None
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            self.object = self.form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.get(request,*args,**kwargs)
    # def post(self, request, *args, **kwargs):
    #     return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # context增加modelform表格数据
        context = super(FormListView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        # 返回model 的field名称
        context['field_meta'] = self.model._meta.fields
        return context


# @method_decorator(login_required)
class GenericDelView(SuperuserRequiredMixin,DeleteView):
    template_name = 'generic/confirm_delete.html'

    def get_context_data(self, *args, **kwargs):
        #context 返回 success_url
        context = super(GenericDelView, self).get_context_data(*args, **kwargs)
        context['success_url'] = self.get_success_url()
        # print context['success_url']
        return context

    def get_object(self, *args, **kwargs):
        object = super(GenericDelView, self).get_object(*args, **kwargs)
        if object:
            # print type(object)
            return object
        else:
            raise Http404

    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.get_success_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(GenericDelView, self).post(request, *args, **kwargs)


# @method_decorator(permission_required)
class GenericUpdateView(SuperuserRequiredMixin,UpdateView):
    template_name = 'generic/update.html'

    def get_context_data(self, *args, **kwargs):
        #context 返回 success_url
        context = super(GenericUpdateView, self).get_context_data(*args, **kwargs)
        context['success_url'] = self.get_success_url()
        context['name'] = self.object
        # print context['success_url']
        return context

    def get_object(self, *args, **kwargs):
        object = super(GenericUpdateView, self).get_object(*args, **kwargs)
        if object:
            return object
        else:
            raise Http404



class GenericListDetailView(DetailView,ListView):
    pass
