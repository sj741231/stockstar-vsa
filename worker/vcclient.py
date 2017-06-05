# -*- coding: utf-8 -*-
__author__ = 'songtao'


import os
import os.path
import time
import socket
import sys
import string
import ssl
import base64
from pysphere import VIServer
from pysphere import VIException, VIApiException, FaultTypes
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
import datetime
#import esxi_exception

import django

cur_path = os.path.abspath(os.path.dirname(__file__))
# print cur_path
par_path = os.path.realpath(os.path.dirname(cur_path))
# print par_path
sys.path.append(par_path)
os.chdir(par_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from django.utils import timezone
from vcenter.models import *
from vsa.settings import VCENTER,VCENTERUSER,VCENTERPASSWD



#to resolve the ssl problem
#import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#Server Control
class VCenterManagement:
    server_ip    = ''
    user_name    = ''
    password     = ''
    connect_flag = False
    server       = None
    #vm_list      = []

    #def __init__(self):

    #Use the given args to connect the esxi server you want
    #@ip[string]: ESXi server's IP address
    #@name[string]: the username used to login the ESXi server
    #@pwd[string]: the password used to login the ESXi server
    def connect_server(self, ip, name, pwd):
        self.server_ip = ip
        self.user_name = name
        self.password  = pwd
        self.server = VIServer()
        self.server.connect(self.server_ip, self.user_name, self.password)
        self.connect_flag = self.server.is_connected()
        if self.connect_flag:
            return True
        return False

    #To get all the definition registered vms from the connected server
    #@param[string]: can be set as ALL, POWER_ON, POWER_OFF, SUSPENDED
    #According to the param, returns a list of VM Paths. You might also filter by datacenter,
    #cluster, or resource pool by providing their name or MORs.
    #if  cluster is set, datacenter is ignored, and if resource pool is set
    #both, datacenter and cluster are ignored.
    def get_registered_vms(self, param, status=None, datacenter=None, cluster=None,
                           resource_pool=None):
        if param not in ['ALL', 'POWER_ON', 'POWER_OFF', 'SUSPENDED']:
            print "Get VMs error: param can only be set as ALL, POWER_ON, POWER_OFF, or SUSPENDED."
            return None
        if self.connect_flag == False:
            print "Get VMs error: Server not connected."
            return None
        if param == 'ALL':
            return self.server.get_registered_vms(datacenter, cluster, resource_pool)
        elif param == 'POWER_ON':
            return self.server.get_registered_vms(datacenter, cluster, resource_pool, status='poweredOn')
        elif param == 'POWER_OFF':
            return self.server.get_registered_vms(datacenter, cluster, resource_pool, status='poweredOff')
        elif param == 'SUSPENDED':
            return self.server.get_registered_vms(datacenter, cluster, resource_pool, status='suspended')
        else:
            return None

    #Disconnect to the Server
    def disconnect(self):
        if self.connect_flag == True:
            self.server = self.server.disconnect()
            self.connect_flag == False

    #To keep session alive
    def keep_session_alive(self):
        assert self.server.keep_session_alive()

    #To get the server type
    def get_server_type(self):
        return self.server.get_server_type()

    #To get performance manager
    def get_performance_manager(self):
        return self.server.get_performance_manager()

    #To get the all the server's hosts
    def get_all_hosts(self):
        """
        Returns a dictionary of the existing hosts keys are their names
        and values their ManagedObjectReference object.
        """
        return self.server.get_hosts()

    #To get all datastores
    def get_all_datastores(self):
        """
        Returns a dictionary of the existing datastores. Keys are
        ManagedObjectReference and values datastore names.
        """
        return self.server.get_datastores()

    #To get all clusters
    def get_all_clusters(self):
        """
        Returns a dictionary of the existing clusters. Keys are their
        ManagedObjectReference objects and values their names.
        """
        return self.server.get_clusters()

    #To get all datacenters
    def get_all_datacenters(self):
        """
        Returns a dictionary of the existing datacenters. keys are their
        ManagedObjectReference objects and values their names.
        """
        return self.server.get_datacenters()

    #To get all resource pools
    def get_all_resource_pools(self):
        """
        Returns a dictionary of the existing ResourcePools. keys are their
        ManagedObjectReference objects and values their full path names.
        """
        return self.server.get_resource_pools()

    #To get hosts by name
    def get_hosts_by_name(self, from_mor):
        """
        Returns a dictionary of the existing ResourcePools. keys are their
        ManagedObjectReference objects and values their full path names.
        @from_mor: if given, retrieves the hosts contained within the specified
            managed entity.
        """
        try:
            hosts_dic = self.server.get_hosts(from_mor)
        except:
            print "Get hosts error!"
            return None
        return hosts_dic

    def get_vm_by_name(self,vm_name):
        try:
            vm = self.server.get_vm_by_name(vm_name)
        except:
            print "Get vm error!"
            return None
        return vm

    def power_on_vm(self,vm_name):
        try:
            vm = self.get_vm_by_name(vm_name)
            if(vm.is_powered_off()):
                vm.power_on()
                print "vm " + vm_name + " power on success."
            else:
                print "vm " + vm_name + "is already power on"
                return False
        except:
            print "Power on vm " + vm_name + "error"
            return False
        return True

    def power_off_vm(self,vm_name):
        try:
            vm = self.get_vm_by_name(vm_name)
            if(vm.is_powered_on()):
                vm.power_off()
                print "vm " + vm_name + " power off success."
            else:
                print "vm " + vm_name + "is already power off"
                return False
        except:
            print "Power off vm " + vm_name + " error"
            return False
        return True

import json


def getdiskinfo(datastore):
    disk_list = []
    for disk in datastore:
        name = disk.name
        size = disk.summary.capacity
        disk_list.append({name:str(size)})
    return json.dumps(disk_list)


def getVmByHost(vm):
    if isinstance(vm,vim.VirtualMachine):
        summary = vm.summary
        cpu = summary.config.numCpu
        # disk = getdiskinfo(vm.datastore)
        tag = json.dumps(getvmtag(vm.availableField, summary.customValue))
        system = summary.guest.guestFullName
        vmdetail = {'vmuuid':summary.config.uuid,'name':vm.name,'ip':summary.guest.ipAddress,'cpu':cpu,'memory':summary.config.memorySizeMB,
                    'system':system,'tag':tag}
        # print vmdetail
        return vmdetail

def gethostinfo(vm,dt_name,depth=1):
    dt =dt_name
    maxdepth = 10
    if hasattr(vm,'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            gethostinfo(c,dt,depth+1)
        return
    if isinstance(vm,vim.ComputeResource):
        cpu = '%sxC %sxT' %(vm.summary.numCpuCores,vm.summary.numCpuThreads)
        disk = getdiskinfo(vm.datastore)
        hostdetail = {'name':vm.name,'ip':vm.name,'cpu':cpu,'memory':vm.summary.totalMemory,'disk':disk}
        hostdetail['esxi_groups'] = datacenter.objects.get(name=dt_name)
        if host.objects.filter(name=vm.name):
            host.objects.filter(name=vm.name).update(**hostdetail)
            h_server = host.objects.get(name=vm.name)
        else:
            h_server = host.objects.create(**hostdetail)

        hostvm = vm.host
        for h in hostvm:
            for v in h.vm:
                result = getVmByHost(v)
                result['esxi'] = h_server
                result['updatetime']= timezone.now()
                if virtualhost.objects.filter(vmuuid=result['vmuuid']):
                    virtualhost.objects.filter(vmuuid=result['vmuuid']).update(**result)
                else:
                    virtualhost.objects.create(**result)
                # try:
                #     virtualhost.objects.filter(vmuuid=result['vmuuid']).update(**result)
                #     print 'update %s' %result
                #     v_host.objects.update(**result)
                # except:
                #     if not virtualhost.objects.filter(vmuuid=result['vmuuid']):
                #         print 'create : %s' %result
                #         v_host = virtualhost.objects.create(**result)


def getvmtag(availiblefield,customvalue):
    field_dict = {}
    for i in availiblefield:
        field_dict[i.key] = i.name
    # if isinstance(customvalue,vim.CustomFieldsManager):
    return [{field_dict[x.key]:x.value} for x in customvalue]
    # return '_'.join([x.value for x in customvalue])



def getvminfo(vm,depth=1):
    maxdepth = 10
    if hasattr(vm,'childEntity'):
        if depth >maxdepth:
            return
        vmList =vm.childEntity
        for vm in vmList:
            getvminfo(vm,depth+1)
    if isinstance(vm,vim.VirtualMachine):
        summary = vm.summary
        cpu = summary.config.numCpu
        disk = getdiskinfo(vm.datastore)
        tag = getvmtag(summary.customValue)
        system = summary.guest.guestFullName
        vmdetail = {'name':vm.name,'ip':summary.guest.ipAddress,'cpu':cpu,'memory':summary.config.memorySizeMB,
                    'disk':disk,'system':system,'tag':tag}
        print vmdetail
        return vmdetail



def getinformation(entry,folder_type,depth=1):
    if folder_type =='vm':
        instancetype = vim.VirtualMachine
    else:
        instancetype = vim.ComputeResource
    maxdepth = 10
    if hasattr(entry,'childEntiry'):
        if depth >maxdepth:
            return
        entryList = entry.childEntiry
        for entry in entryList:
            getinformation(entry,folder_type,depth+1)
    if isinstance(entry,instancetype):
        summary = entry.summary



def test():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    ssl_context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=VCENTER,user=VCENTERUSER,pwd=VCENTERPASSWD,sslContext=ssl_context)
    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child,'hostFolder'):
            dt = child
            datacenter.objects.update_or_create(**{'name':dt.name})
            hostFolder = dt.hostFolder
            entitylist = hostFolder.childEntity
            for l in entitylist:
                hostinfo = gethostinfo(l,dt.name)




def test1():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    ssl_context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=VCENTER,user=VCENTERUSER,pwd=VCENTERPASSWD,sslContext=ssl_context)
    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child,'vmFolder'):
            dt = child
            # print datacenter.objects.update_or_create(**{'name':dt.name})
            vmFolder = dt.vmFolder
            entitylist = vmFolder.childEntity
            for l in entitylist:
                hostinfo = getvminfo(l)




if __name__ == "__main__":
    test()
