# -*- coding: utf-8 -*-
__author__ = 'songtao'

import os
import sys
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






def sendmail():

    mail_to = ["bjhtmg@zhengjin99.com","bjszmarketmg@zhengjin99.com","litao.zhao@zhengjin99.com","market@zhengjin99.com",
"tdmg@zhengjin99.com","tgmg@zhengjin99.com"]

    subject = u'系统运维联系人'
    mail_msg = u"""
各位同事，大家好！

       为能够快速定位问题、解决问题、提高问题处理的响应速度，以下为系统运维人员联系方式，各办公区桌面问题,视频直播问题，坐席系统等问题第一时间联系对应区域技术支持人员处理或反馈，视频网站问题可以随时联系谢玉松，宋涛处理，呼叫中心问题可以随时联系刘洋，马亮处理，网络问题可以随时联系许诗玉，邮件、rtx问题可以随时联系刘旸处理。



联系人                       联系电话
董乐   (运维负责人)          18501340727
谢玉松 (网站运维)            18701089077
刘洋   (呼叫中心运维)        18618269329
马亮   (重庆系统运维)        18600906752
廖建伟 (深圳系统运维)          17770142501
刘旸   (系统运维)            15210952712
许诗玉 (网络运维)            13011109321
赵宇   (庄胜技术支持)        17310785351
桑小强 (南翼7层技术支持)     18732505621
杨硕   (庄胜技术支持)        15132156883
贾中锋 (雍贵技术支持)        13333311874
陈延禄 (陶然亭技术支持)      13120492335

    """
    msg = EmailMultiAlternatives(subject,mail_msg,to=mail_to)
    msg.send()





sendmail()
