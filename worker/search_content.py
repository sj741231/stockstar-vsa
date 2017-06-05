# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymongo
import json
import sys
import datetime
import csv
import os
from pandas import DataFrame,Series
import pandas as pd
import django

# 初始化环境变量
cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()


from django.core.mail import EmailMultiAlternatives,EmailMessage


reload(sys)
sys.setdefaultencoding('utf-8')

now = datetime.datetime.now()


def get_mongodb_content():
    host = ['10.99.12.53','10.99.12.54']
    db_name = 'mongodb'
    conn = pymongo.MongoClient(host)
    db = conn.get_database(db_name,read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED)
    result = db.chat.find({"createdate" : now.strftime('%Y-%m-%d')},{'createdate':1,'createtime':1,'fromuser':1,'content':1})
    return result


def sendmail(useremail,attachment_file):
    '''
    发送带有附件的邮件,mimetype 必须为application/octet-stream
    '''
    subject = u"用户聊天统计--%s" %(now.strftime('%Y-%m-%d') )
    mail_msg = u"用户聊天统计--%s" %(now.strftime('%Y-%m-%d'))
    msg = EmailMultiAlternatives(subject,mail_msg,to=[useremail])
    msg.attach_file(attachment_file, mimetype='application/octet-stream')
    msg.send()



if __name__ == "__main__":
    result = get_mongodb_content()
    # header = [u'日期',u'时间',u'用户id',u'聊天内容']
    # rows = []
    fields = ['createdate','createtime','fromuser','content']
    df = pd.DataFrame(list(result),columns=fields)
    filename = now.strftime('%Y-%m-%d %H-%M') + '.xls'
    filepath = par_path + '/' + filename
    df.to_excel(filepath,sheet_name='sheet1')

    sendmail('le.dong@zhengjin99.com',filepath)
    sendmail('tao.song@zhengjin99.com',filepath)
