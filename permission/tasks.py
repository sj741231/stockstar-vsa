# -*- coding: utf-8 -*-
__author__ = 'songtao'

import os
from Crypto.PublicKey import RSA
from vsa.celery import app
from vsa.settings import DEPLOYUSER

from ansible.inventory import Inventory
from ansible.runner import Runner
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from permission.models import User_Host
from accounts.tasks import bash, is_dir


def list_user_hosts(perm_id):
    perm = User_Host.objects.get(id=perm_id)
    hostlist = []
    for h in perm.host.all():
        hostlist.append(str(h.ip))
    for hg in perm.hostgroup.all():
        for i in hg.host_set.all():
            hostlist.append(str(i.ip))
    return list(set(hostlist))


def gen_ssh_key(username, password=None, length=2048):
    """
    create user's home and create private key and public key
    :param username:
    :param password:
    :param length:
    """
    private_key_dir = '/home/%s/.ssh/' % username
    private_key_file = os.path.join(private_key_dir, "id_rsa")
    public_key_dir = '/home/%s/.ssh/' % username
    public_key_file = os.path.join(public_key_dir, 'id_rsa.pub')
    is_dir(private_key_dir, username, mode=0700)
    is_dir(public_key_dir, username, mode=0700)
    key = RSA.generate(length)
    with open(private_key_file, 'w') as pri_f:
        pri_f.write(key.exportKey('PEM', password))
    os.chmod(private_key_file, 0600)
    pub_key = key.publickey()
    with open(public_key_file, 'w') as pub_f:
        pub_f.write(pub_key.exportKey('OpenSSH'))
    os.chmod(public_key_file, 0600)
    bash('chown %s:%s %s' % (username, username, public_key_file))
    bash('chown %s:%s %s' % (username, username, private_key_file))

    return private_key_file, public_key_file


# @app.task(name='add_perm', time_limit=600)
# def add_perm(perm_id):
#     perm = User_Host.objects.get(id=perm_id)
#     username = perm.user.username
#     hostlist = list_user_hosts(perm_id)
#     key_path = "/home/%s/.ssh/id_rsa.pub" % username
#     if not os.path.exists(key_path):
#         gen_ssh_key(username=username)
#     arg = 'name=%s' % perm.user.username
#     arg1 = 'path=/home/%s/.ssh state=directory owner=%s group=%s mode=0700' % (username, username, username)
#     arg2 = 'src=/home/%s/.ssh/id_rsa.pub dest=/home/%s/.ssh/authorized_keys owner=%s mode=600 group=%s' \
#            % (username, username, username, username)
#     arg3 = "dest=/etc/sudoers state=present regexp='^%s' line='%s ALL=(ALL) NOPASSWD: ALL'" % (username, username)
#     result = []
#     for i in hostlist:
#         add_user = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
#                           become_method='sudo',
#                           module_name='user', module_args=arg).run()
#         result.append(add_user)
#         if add_user:
#             mk_dir = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
#                             become_method='sudo',
#                             module_name='file', module_args=arg1).run()
#             result.append(mk_dir)
#             copy_pubkey = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER,
#                                  become=True,
#                                  become_method='sudo',
#                                  module_name='copy', module_args=arg2).run()
#             result.append(copy_pubkey)
#             sudo = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
#                           become_method='sudo',
#                           module_name='lineinfile', module_args=arg3).run()
#             result.append(sudo)
#     print result
#     return result


@app.task(name='add_perm', time_limit=600)
def add_perm(username,ip):
    key_path = "/home/%s/.ssh/id_rsa.pub" % username
    if not os.path.exists(key_path):
        gen_ssh_key(username=username)
    arg = 'name=%s' % username
    arg1 = 'path=/home/%s/.ssh state=directory owner=%s group=%s mode=0700' % (username, username, username)
    arg2 = 'src=/home/%s/.ssh/id_rsa.pub dest=/home/%s/.ssh/authorized_keys owner=%s mode=600 group=%s' \
           % (username, username, username, username)
    arg3 = "dest=/etc/sudoers state=present regexp='^%s' line='%s ALL=(ALL) NOPASSWD: ALL'" % (username, username)
    result = []
    add_user = Runner(inventory=Inventory([ip]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                      become_method='sudo',
                      module_name='user', module_args=arg).run()
    result.append(add_user)
    if add_user:
        mk_dir = Runner(inventory=Inventory([ip]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                        become_method='sudo',
                        module_name='file', module_args=arg1).run()
        result.append(mk_dir)
        copy_pubkey = Runner(inventory=Inventory([ip]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER,
                             become=True,
                             become_method='sudo',
                             module_name='copy', module_args=arg2).run()
        result.append(copy_pubkey)
        sudo = Runner(inventory=Inventory([ip]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                      become_method='sudo',
                      module_name='lineinfile', module_args=arg3).run()
        result.append(sudo)
    return result



@app.task(name='refresh_key', time_limit=600)
def refresh_key(perm_id):
    perm = User_Host.objects.get(id=perm_id)
    username = perm.user.username
    hostlist = list_user_hosts(perm_id)
    # key_path = "/home/%s/.ssh/id_rsa.pub" % username
    gen_ssh_key(username=username)
    arg = 'name=%s' % perm.user.username
    arg1 = 'path=/home/%s/.ssh state=directory owner=%s group=%s mode=0700' % (username, username, username)
    arg2 = 'src=/home/%s/.ssh/id_rsa.pub dest=/home/%s/.ssh/authorized_keys owner=%s mode=600 group=%s' % (
        username, username, username, username)
    result = []
    for i in hostlist:
        print i
        add_user = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                          become_method='sudo',
                          module_name='user', module_args=arg).run()
        result.append(add_user)
        mk_dir = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                        become_method='sudo',
                        module_name='file', module_args=arg1).run()
        result.append(mk_dir)
        copy_pubkey = Runner(inventory=Inventory([i]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                             become_method='sudo',
                             module_name='copy', module_args=arg2).run()
        result.append(copy_pubkey)
    return result


@app.task(name='SyncKey', time_limit=30)
def SyncKey(username, ip):
    # arg1 = 'path=/home/%s/.ssh state=directory owner=%s group=%s mode=0700' % (username, username, username)
    arg2 = 'src=/home/%s/.ssh/id_rsa.pub dest=/home/%s/.ssh/authorized_keys owner=%s mode=600 group=%s' % (
        username, username, username, username)
    result = []
    # mk_dir = Runner(inventory=Inventory([ip]), forks=1, remote_user=DEPLOYUSER, become=True, become_method='sudo',
    #                 module_name='file', module_args=arg1).run()
    # result.append(mk_dir)
    copy_pubkey = Runner(inventory=Inventory([ip]), remote_port=22022, timeout=5, forks=1, remote_user=DEPLOYUSER, become=True,
                         become_method='sudo', module_name='copy', module_args=arg2).run()
    result.append(copy_pubkey)
    return result
