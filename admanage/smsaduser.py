# -*-coding=utf8-*-
__author__ = 'shijin'

import os
import sys
import urllib
import urllib2
import requests
#from django.core.mail import EmailMultiAlternatives,EmailMessage
#from vsa.celery import app
#from celery.utils.log import get_task_logger
path = os.getcwd()
parent_path = os.path.dirname(path)
sys.path.append(parent_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vsa.settings")

#os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
import django
django.setup()

from admanage.models import *

#edit by shijin
''' 
def sms_aduser():
    
    1.通过短信URL接口发送ad新用户邮箱和RTX帐号、密码
    2.adusers获取临时表中sendstatus=False 数据。
    2.使用requests模块，POST方式调用短信接口，发送adusers数据，如果返回值是200，那么更新数据sendstatus=True
    
    url = 'http://sms.zhengjin99.com/SMS/send.jsp'
    adusers = SmsAdUser.objects.filter(sendstatus = False)
    for smsuser in adusers:
        #print smsuser.id,smsuser.aduser,smsuser.mobile
        if  smsuser.mobile:
            
            password = '34er#$ER'
            pwdurl = 'http://172.16.33.132/iisadmpwd/'
            msg = u'%s您好，您的邮箱及RTX账号: %s已开通，默认密码为：%s ，为保证账户信息安全，请登录修改初始密码%s  ' % (smsuser.aduser,smsuser.adaccount,password,pwdurl)

            context1 = msg.encode('utf-8')
            context = urllib.quote(context1)
            #print context
            p2 = u'系统运维部'
            p2 = urllib.quote(p2.encode('utf-8'))

            data= dict(mobile=str(smsuser.mobile),tpl='301',p1=context,p2=p2)
            #print data

            r = requests.post(url,data=data)
            
            if str(r.status_code) == '200':

                smsuser.sendstatus = True
                smsuser.save()
            #print r.text

    #return {'result':r.text}
'''    
    
#edit by shijin 证金短信通道
def sms_aduser(**smsuser):
    '''
    1.通过短信URL接口发送ad新用户邮箱和RTX帐号、密码
    2.adusers获取临时表中sendstatus=False 数据。
    2.使用requests模块，POST方式调用短信接口，发送adusers数据，如果返回值是200，那么更新数据sendstatus=True
    '''
    #aduser = t[0], adaccount = account, department = t[1], aduserfile = xls_file, mobile = str(int(t[4])), sendstatus = False,smsuser.deltail=''

    #print smsuser
    print smsuser['aduser'],smsuser['adaccount'],smsuser['department'],smsuser['aduserfile'],smsuser['mobile'],smsuser['sendstatus'],smsuser['detail']

    url = 'http://sms.zhengjin99.com/SMS/send.jsp'

    if  smsuser['mobile']:
        aduser = SmsAdUser.objects.create(**smsuser)
            
        password = '34er#$ER'
        pwdurl = 'http://172.16.33.132/iisadmpwd/'
        msg = u'%s您好，您的邮箱及RTX账号: %s已开通，默认密码为：%s ，为保证账户信息安全，请登录修改初始密码%s  ' % (smsuser['aduser'],smsuser['adaccount'],password,pwdurl)

        context1 = msg.encode('utf-8')
        context = urllib.quote(context1)
            #print context
        p2 = u'系统运维部'
        p2 = urllib.quote(p2.encode('utf-8'))

        data= dict(mobile=str(smsuser['mobile']),tpl='301',p1=context,p2=p2)
            #print data

        r = requests.post(url,data=data)
            
        if r.text:
            aduser.sendstatus = True           
            aduser.detail = r.text
            aduser.save()
            #print r.text

    #return {'result':r.text}
    
#edit by shijin 上证综研短信通道，延时3分钟左右。
def sms_aduser1(**smsuser):
    '''
    1.通过短信URL接口发送ad新用户邮箱和RTX帐号、密码
    2.根据传入参数，设置短信接口需要的手机号，内容＋【上证综研】,user:zj_67,pass:3laa801k
    3.使用requests模块，POST方式调用短信接口，发送adusers数据，如果返回值是200，那么更新数据sendstatus=True,存入接口返回信息aduser.detail
    '''
    #aduser = t[0], adaccount = account, department = t[1], aduserfile = xls_file, mobile = str(int(t[4])), sendstatus = False,smsuser.deltail=''

    #print smsuser
    print smsuser['aduser'],smsuser['adaccount'],smsuser['department'],smsuser['aduserfile'],smsuser['mobile'],smsuser['sendstatus'],smsuser['detail']

    url = 'http://sms.zhengjin99.com/SMS/send_jrj.jsp'

    if  smsuser['mobile']:
        aduser = SmsAdUser.objects.create(**smsuser)
            
        password = '34er#$ER'
        pwdurl = 'http://172.16.33.132/iisadmpwd/'
        msg = u'%s您好，您的邮箱及RTX账号: %s已开通，默认密码为：%s ，为保证账户信息安全，请登录修改初始密码%s【上证综研】' % (smsuser['aduser'],smsuser['adaccount'],password,pwdurl)

        context1 = msg.encode('utf-8')
        context = urllib.quote(context1)
            #print context
        #p2 = u'系统运维部'
        #p2 = urllib.quote(p2.encode('utf-8'))
        
        data={}
        data['mobile'] = str(int(smsuser['mobile']))
        data['content'] = context
        data['user'] = 'zj_67'
        data['pass'] = '3laa801k'

        #data= dict(mobile=str(smsuser['mobile']),tpl='301',p1=context,p2=p2)
        print data
        
        r = requests.post(url,data=data)
            
        if r.text:
            aduser.sendstatus = True           
            aduser.detail = r.text
            aduser.save()
            #print r.text
         
    #return {'result':r.text}  


if  __name__  == "__main__":
    dct = {'aduser': 'shijin', 'mobile': '13701393884', 'adaccount': 'jin.shi', 'aduserfile': 'test.excel', 'department': 'systemp devops', 'sendstatus': False ,'detail':''}
    #sms_aduser(**dct)
    sms_aduser1(**dct)
