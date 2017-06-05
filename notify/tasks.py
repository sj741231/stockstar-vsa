# -*-coding=utf8-*-
import os
import sys
import urllib
import urllib2
import requests
from django.core.mail import EmailMultiAlternatives,EmailMessage
from vsa.celery import app
from celery.utils.log import get_task_logger
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from notify.models import *
url = 'http://sms.zhengjin99.com/SMS/send.jsp'
# url = "http://sms.zhengjin99.com/SMS/send_jrj.jsp?user=jrj&pass=1234&mobile=13621315559&content="

def sendmail(username,useremail,passwd,rsa_file):

    subject = u'跳板机系统通知'
    mail_msg = u"""
    证金跳板机系统--通知
    跳板机地址：10.99.12.80
    用户名：%s
    附件为私钥文件
    私钥密码:%s
    xshell 与 crt 配置方法
    http://10.99.12.80:8080/static/88888-12124391-130716-1129-3.pdf
    注意！！！ 在使用过程中如遇到什么问题，请及时向运维部反馈，谢谢配合。
    """ % (username, passwd, )
    msg = EmailMultiAlternatives(subject,mail_msg,to=[useremail])
    msg.attach_file(rsa_file,mimetype='text/plain')
    msg.send()
    # email = EmailMessage(subject, mail_msg, to=[useremail])
    # email.attach_file(rsa_file,mimetype="text/html")
    # mail_status = email.send()



logger = get_task_logger(__name__)



@app.task(name="notify_user_by_sms")
def notify_user(userid,msg):
    user = NotifyUser.objects.get(id=str(userid))
    context1 = msg.encode('utf-8')
    context = urllib.quote(context1)
    print context
    p2 = u'系统运维部'
    p2 = urllib.quote(p2.encode('utf-8'))

    data= dict(mobile=str(user.telephone),tpl='301',p1=context,p2=p2)
    # print data
    print data
    #
    r = requests.post(url,data=data)
    if r.text:
        NotifyLog.objects.create(notifyuser=user,notifymsg=msg)

    return {'result':r.text}



@app.task(name="notify_users_by_sms")
def notify_users(userlist,msg):
    result = []
    users = NotifyUser.objects.filter(pk__in=userlist)
    usernames = users.values_list('username',flat=True)
    for user in users:
        context1 = msg.encode('utf-8')
        context = urllib.quote(context1)
        print context
        p2 = u'系统运维部'
        p2 = urllib.quote(p2.encode('utf-8'))
        data= dict(mobile=str(user.telephone),tpl='301',p1=context,p2=p2)
        r = requests.post(url,data=data)
        result.append({user.username:r.text})
    NotifyLog.objects.create(notifymsg=msg,notifyusers=usernames,detail=result)
    return {'result':result}




