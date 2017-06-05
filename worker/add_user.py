import os
import sys
import django

cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from server.models import *
from permission.models import *
from django.contrib.auth.models import User

username = sys.argv[1]
f_path = sys.argv[2]
user = User.objects.get(username=username)

u_h,flug = User_Host.objects.get_or_create(user=user)
print flug

f = open(f_path)
ip_list = []
for i in f.readlines():
    ip = i.split("  ")[-1].rstrip('\n')
    try:
        host = Host.objects.get(ip=ip)
        u_h.host.add(host)
    except:
        print 'user:%s add %s fail' %(user.username,ip)
