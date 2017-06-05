# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import NotifyForm
from .models import NotifyUser,NotifyLog
from .tasks import notify_users


#shijin edit
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from  admanage.models import AdAddUserLog
from .forms import NotifyADuserForm

@login_required()
def notify(request):
    notifyusers = NotifyUser.objects.all()
    form = NotifyForm()
    if request.method == "POST":
        form = NotifyForm(request.POST)
        if form.is_valid():
            users = request.POST.getlist('users')
            message = request.POST.get('message')
            notify_users.delay(users,message)
            return HttpResponse("<script> alert('" + u'通知中' + "');window.location.href='/notify/log'</script>")

    return render(request,'notify.html',locals())



#edit by shijin
def sms_ad_user(request):
    '''
    1.设置errors列表为空
    2.判断request == "POST"；判断aduserfile的value是否为空，如为空errors增加错误提示。
    3.如果errors为空，那么根据“aduserfile”模糊检索出AdAddUserLog数据库对象，返回查询结果smsresult.html
    4.如果request.method != POST,那么返回表单页smssearch.html，默认第一次直接返回表单页且errors为空。
    '''
    errors=[]
    if request.method == 'POST':
        if not request.POST.get('aduserfile'):
            errors.append("请输入模板文件名称或日期模糊查询")
            
        if not errors:
            aduserdata=AdAddUserLog.objects.filter(aduserfile__contains=request.POST.get('aduserfile'))      
         
            return render(request,'smsresult.html',{'aduserdata':aduserdata})
        
    return render(request,'smssearch.html',{'errors':errors})


def sms_ad_send(request):
    '''
    '''
    if request.method == 'POST':
        sms_form = NotifyADuserForm(request.POST)
        if sms_form.is_valid():
            aduser_value = request.POST.getlist('aduser')
            adaccount_value = request.POST.get('adaccount')
            message_value = request.POST.get('message')
            mobile_value = request.POST.get('mobile')
            
            return HttpResponse("测试Forms成功！")
    else:
        sms_form = NotifyADuserForm()
    return render(request, 'smssend.html', {'sms_form': sms_form})
                
            
