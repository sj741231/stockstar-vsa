# -*- coding: utf-8 -*-


from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

from vsa.genericviews import FormListView
from django.core.urlresolvers import reverse_lazy
from .models import *
from .forms import *
from .utils import uploadgrouprelation
from tasks import adadduser
#edit by shijin
from .smsaduser import sms_aduser

# Create your views here.

@staff_member_required()
def upload_group_from_xls(request):
    if request.method == 'POST':
        fileexcel = request.FILES['file']
        myexcel = open('upload/groups.xls', 'w')
        for chunk in fileexcel.chunks():
            myexcel.write(chunk)
        myexcel.close()
        failhost = uploadgrouprelation(xlsfile='upload/groups.xls')
        return HttpResponseRedirect('/admanage/grouprelation')
    return render(request,'xls_upload.html',locals())


class AdUserFileView(FormListView):
    form_class = AduserFileForm
    template_name = 'aduserfile.html'
    model = AdUserfile

    # def get_initial(self):
    #     initial = super(AdUserFileView,self).get_initial()
    #     initial['uploader'] = self.request.user
    #     return initial

    # def get_form_kwargs(self):
    #     kwargs = super(AdUserFileView,self).get_form_kwargs()
    #     kwargs['uploader'] = self.request.user
    #     return kwargs

    def post(self, request, *args, **kwargs):
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            form = self.form.save(commit=False)
            form.uploader = request.user
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return self.get(request, *args, **kwargs)



def push_add_aduser(request,pk):
    xls_file = get_object_or_404(AdUserfile,pk=int(pk))
    filepath = xls_file.xls_file.path
    adadduser.delay(filepath)
    return HttpResponse("<script> alert('" + u'处理中' + "');window.location.href='/admanage/addaduser/log'</script>")

def sjtest(request):
    return HttpResponse("石进测试py更新生效 2017-06-09-001")