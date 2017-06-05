# -*- coding: utf-8 -*-


import subprocess
import pprint
import sys
import os
import pexpect
import struct, fcntl, termios, signal
import getpass
import time
import logging
import re
import django
from prettytable import PrettyTable
from pandas import Series,DataFrame

# from django.core.validators import _lazy_re_compile

# 初始化环境变量
cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from server.models import *
from django.contrib.auth.models import User
from vcenter.models import virtualhost

logging.basicConfig()

ipv4_re = '^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z'

logpath = '/data/userlog'
now = time.localtime()
today_log_path = logpath + '/' + time.strftime('%Y%m%d', now)


class timestampfile(object):
    def __init__(self, file, tm, tmfile):
        self.file = file
        self.tmfile = tmfile
        self.tm1 = time.time()

    def write(self, data):
        # get the data size of bytes
        ts = round(time.time() - self.tm1, 4)
        datasize = data.__sizeof__()
        # ts = datetime.datetime.utcnow().isoformat()
        # return self.file.write("%s %s\n" %(ts,data))
        with open(self.tmfile, 'a') as f:
            f.write('%s %s\n' % (ts, datasize))
        self.tm1 = time.time()
        return self.file.write(data)

    def flush(self):
        self.file.flush()


def Create_log_path(username):
    now = time.localtime()
    today_log_path = logpath + '/' + username + '/' + time.strftime('%Y%m%d', now)
    if not os.path.exists(today_log_path):
        os.makedirs(today_log_path)
        return today_log_path
    else:
        return today_log_path


def sigwinch_passthrough(sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(),
                                          termios.TIOCGWINSZ, s))
    global p
    p.setwinsize(a[0], a[1])


def get_hostlist(username):
    user = User.objects.get(username=username)
    h_dict = {}
    h_list = []
    try:
        if 'op' in user.groups.all().values_list('name',flat=True):
            hosts = Host.objects.all()
        else:
            hosts = user.user_host.host.all()
        for h in hosts:
            h_dict[str(h.id)] = str(h.ip)
            h_list.append(str(h.ip))
        for g in user.user_host.hostgroup.all():
            for x in g.host_set.all():
                h_dict[str(x.id)] = str(x.ip)
                h_list.append(str(x.ip))
    except:
        pass
    h_list = list(set(h_list))
    sorted(h_list)
    return h_dict, h_list


def user_host(username):
    '''

    :param username:
    :return:
    '''
    user = User.objects.get(username=username)
    print user.groups.all().values_list('name',flat=True)
    if 'op' in user.groups.all().values_list('name',flat=True):
        return virtualhost.objects.all()
    else:
        perms = user.userperm_set.all()
        return [perm.host for perm in perms]


def printhostlist(hostlist):
    '''

    :param hostlist: host object in list
    :return:
    '''
    t= PrettyTable([u'id',u'主机名',u'ip地址'])
    for i in hostlist:
        t.add_row([i.id,i.name,i.ip])
    print t



def run_sh(cmd):
    """run shell script"""
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if pipe.stdout:
        stdout = pipe.stdout.read().strip()
        pipe.wait()
        return stdout
    if pipe.stderr:
        stderr = pipe.stderr.read()
        pipe.wait()
        return stderr


def help(width=80):
    print '\033[1;32m欢迎使用证金跳板机\033[0m'.center(width, '#')

    print '\033[32m直接输入服务器编号或ip地址登陆.\033[0m'.ljust(4)
    print """
    h|H) 帮助
    q|Q) 退出
    l|L) 列出可用主机
    l3|L3) 分3列出主机
"""


def format_hostlist(h_list):
    '''
    :param h_list: [10.99.12.150,10.99.13.43]
    :print
        +------+---------------+
        | 编号 |     ip地址    |
        +------+---------------+
        |  0   |  10.99.12.150 |
        |  1   |  10.99.13.43  |
        |  2   |  10.99.13.48  |
        |  3   |  10.99.12.89  |
        |  4   | 10.100.10.119 |
        |  5   | 10.100.10.145 |
        +------+---------------+

    '''

    t= PrettyTable([u'编号',u'ip地址'])
    if isinstance(h_list,list):
        for i, k in enumerate(h_list):
            t.add_row([i,k])
        print t


def format_hostlist3(h_list):
    p_list = []
    if isinstance(h_list,list):
        for i, k in enumerate(h_list):
            msg = '%s -> %s' %(i,k)
            p_list.append(msg)
    # print p_list
    new_p_list = [p_list[x:x+3] for x in xrange(0,len(p_list),3)]
    for row in new_p_list:
        print "".join(x.ljust(35) for x in row)


def format_hostdic(h_dict):
    for i, k in h_dict.items():
        print i, ':', k



def connect_host(ip, username, rows, cols):
    """url: ssh root@192.168.1.1
       pexpect 方法实现 ssh登陆，交互式处理，记录日志
    """
    user=User.objects.get(username=username)
    if 'op' in user.groups.all().values_list('name',flat=True):
        cmd = 'ssh -i /data/userlog/id_rsa deploy@%s -p 22022 ' %(ip)
    else:
        cmd = 'ssh %s@%s -p 22022' % (username, ip)
    tm = int(time.mktime(time.localtime()))
    userlogfile = '%s_%s.log' % (username, tm)
    usertmfile = '%s_%s.time' % (username, tm)
    userlogpath = Create_log_path(username)
    log = userlogpath + '/' + userlogfile
    tmfile = userlogpath + '/' + usertmfile
    user = User.objects.get(username=username)
    event = Event(user=user, host=Host.objects.get(ip=ip), log=log)
    event.save()
    # size=getwinsize()
    # try:
    global p
    # print cmd
    p = pexpect.spawn(cmd, maxread=4096, dimensions=(rows, cols))
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    # p.interact()
    with open(log, 'a') as f:
        # f.write(('Script started on %s\n' % time.asctime()).encode())
        p.logfile_read = timestampfile(f, tm, tmfile)
        p.interact(escape_character=chr(29))
        # except:
        #    pass


if __name__ == "__main__":
    username = getpass.getuser()
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    hostdict, hlist = get_hostlist(username)
    hostlist = user_host(username)
    help(cols)
    try:
        while 1:
            try:
                option = raw_input("请选择:\n")
                if re.match(ipv4_re, option):
                    if option in hlist:
                        connect_host(option, username, rows, cols)
                elif option in ['l', 'L']:
                    format_hostlist(hlist)
                elif option in ['n', 'N']:
                    printhostlist(hostlist)
                elif option in ['l3', 'L3']:
                    format_hostlist3(hlist)
                elif option in ['q', 'Q', 'e', 'quit', 'exit']:
                    sys.exit()
                elif option in ['h', 'H']:
                    help()
                elif int(option) < len(hlist):
                    ip = hlist[int(option)]
                    connect_host(ip, username, rows, cols)
                    format_hostlist(hostdict)
                else:
                    print "输入有误或未授权ip，请重新输入!\n"
            except (EOFError,ValueError, KeyboardInterrupt):
                help()
                continue
    except IndexError:
        print 'error'
