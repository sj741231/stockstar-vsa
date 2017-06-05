# -*-coding=utf8-*-
import os
import sys
import subprocess
import random
import string
from Crypto.PublicKey import RSA
from django.core.mail import EmailMultiAlternatives,EmailMessage
from vsa.celery import app
from celery.utils.log import get_task_logger
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()


BASE_DIR = "/root/optool"


def bash(cmd):
    """"""
    return subprocess.call(cmd, shell=True)


def is_dir(dir_name, username, mode):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
        bash("chown -R  %s:%s '%s'" % (username, username, dir_name))
    os.chmod(dir_name, mode)


def gen_rand_pwd(num=8):
    """
    :param num:
    :return: random password
    """
    seed = (string.punctuation+string.letters+string.digits)
    # seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+=-[]\;',./{}|:<>?"
    # salt_list = []
    # for i in range(num):
    #     salt_list.append(random.choice(seed))
    salt_list = [random.choice(seed) for i in range(num)]
    salt = ''.join(salt_list)
    return salt


def gen_ssh_key(username, password=None, length=2048):
    """
    create user's home and create private key and public key
    :param username:
    :param password:
    :param length:
    """
    private_key_dir = '/home/%s/.ssh/' % username
    private_key_file = os.path.join(private_key_dir, username+".pem")
    public_key_dir = '/home/%s/.ssh/' % username
    public_key_file = os.path.join(public_key_dir, 'authorized_keys')
    is_dir(private_key_dir,username,mode=0700)
    is_dir(public_key_dir, username, mode=0700)
    key = RSA.generate(length)
    with open(private_key_file, 'w') as pri_f:
        pri_f.write(key.exportKey('PEM', password))
    os.chmod(private_key_file, 0600)
    pub_key = key.publickey()
    with open(public_key_file, 'w') as pub_f:
        pub_f.write(pub_key.exportKey('OpenSSH'))
        pub_f.write('\n')
    os.chmod(public_key_file, 0600)
    bash('chown %s:%s %s' % (username, username, public_key_file))
    return private_key_file



def main():
    username = sys.argv[1]
    passwd = gen_rand_pwd(12)
    pk = gen_ssh_key(username,passwd)
    print username , passwd
    # pass


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

# app = Celery()

@app.task(name="test")
def test(aaa):
    pass


@app.task(name="add_user")
def add_user(username,email):
    cmd = 'useradd -m %s' %username
    print cmd
    bash(cmd)
    passwd = gen_rand_pwd(12)
    pk = gen_ssh_key(username,passwd)
    result=sendmail(username,email,passwd,pk)
    return result




# if __name__ =="__main__":
#     a = gen_ssh_key('songtao','123456')
#     print a
#     sendmail('songtao','tao.song@zhengjin99.com','St@1224',a)
