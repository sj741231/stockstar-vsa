# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.list import ListView,View
from django.views.generic.edit import ModelFormMixin,FormMixin,DeleteView,UpdateView
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from IPy import IP

from models import *
from forms import *
# from templatetags.idc_tags import get_field_verbose_name

def index(request):
    a = 'idc'
    return render_to_response('idc_index.html',locals(),context_instance=RequestContext(request))


class IdcFormListView(ModelFormMixin, ListView):

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        # Explicitly states what get to call:
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 定义post方法，保存form数据,返回idc列表页
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.object = self.form.save()
            # return HttpResponseRedirect('')
            return self.get(self,request)
        else:
            return self.get(request,*args,**kwargs)


    def get_context_data(self, *args, **kwargs):
        # context增加modelform表格数据
        context = super(IdcFormListView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form
        # 返回model 的field名称
        context['field_meta'] = self.model._meta.fields
        return context

    # def get_success_url(self):
    #     return HttpResponseRedirect('/idc')


# class GenericDelView(DeleteView):
#
#     def get_object(self, *args, **kwargs):
#         object = super(GenericDelView,self).get_object(*args, **kwargs)
#         if object:
#             return object
#         else:
#             raise Http404


def ipaddressdetail(request):

    pass


def ip_add(request):
    pass

