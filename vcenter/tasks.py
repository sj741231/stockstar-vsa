# -*- coding: utf-8 -*-
__author__ = 'songtao'

# from __future__ import print_function

import os
import atexit
import argparse
import getpass
import ssl

from pyVim import connect
import django

import vmutils
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import getpass
import ssl
from vsa.celery import app




os.environ['DJANGO_SETTINGS_MODULE'] = 'vsa.settings'
django.setup()

from vsa.settings import VCENTER,VCENTERPASSWD,VCENTERUSER

ssl._create_default_https_context = ssl._create_unverified_context


def virtual_machine_device_info(uuid):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    ssl_context.verify_mode = ssl.CERT_NONE
    si = connect.SmartConnect(host=VCENTER,user=VCENTERUSER,pwd=VCENTERPASSWD,sslContext=ssl_context)
    atexit.register(connect.Disconnect, si)
    search_index = si.content.searchIndex
    # vm = search_index.FindByIp(None, ip, True)
    vm = search_index.FindByUuid(None, uuid, True)

    details = {'name': vm.summary.config.name,
           'instance UUID': vm.summary.config.instanceUuid,
           'bios UUID': vm.summary.config.uuid,
           'path to VM': vm.summary.config.vmPathName,
           'guest OS id': vm.summary.config.guestId,
           'guest OS name': vm.summary.config.guestFullName,
           'host name': vm.runtime.host.name,
           'last booted timestamp': vm.runtime.bootTime}
    for name, value in details.items():
        print("  {0:{width}{base}}: {1}".format(name, value, width=25, base='s'))

    print("  Devices:")
    print("  --------")
    for device in vm.config.hardware.device:
        # diving into each device, we pull out a few interesting bits
        dev_details = {'key': device.key,
                       'summary': device.deviceInfo.summary,
                       'device type': type(device).__name__,
                       'backing type': type(device.backing).__name__}

        print("  label: {0}".format(device.deviceInfo.label))
        print("  ------------------")
        for name, value in dev_details.items():
            print("    {0:{width}{base}}: {1}".format(name, value,
                                                      width=15, base='s'))

        if device.backing is None:
            continue

        # the following is a bit of a hack, but it lets us build a summary
        # without making many assumptions about the backing type, if the
        # backing type has a file name we *know* it's sitting on a datastore
        # and will have to have all of the following attributes.
        if hasattr(device.backing, 'fileName'):
                datastore = device.backing.datastore
                if datastore:
                    print("    datastore")
                    print("        name: {0}".format(datastore.name))
                    # there may be multiple hosts, the host property
                    # is a host mount info type not a host system type
                    # but we can navigate to the host system from there
                    for host_mount in datastore.host:
                        host_system = host_mount.key
                        print("        host: {0}".format(host_system.name))
                    print("        summary")
                    summary = {'capacity': datastore.summary.capacity,
                               'freeSpace': datastore.summary.freeSpace,
                               'file system': datastore.summary.type,
                               'url': datastore.summary.url}
                    for key, val in summary.items():
                        print("            {0}: {1}".format(key, val))
                print("    fileName: {0}".format(device.backing.fileName))
                print("    device ID: {0}".format(device.backing.backingObjectId))

        print("  ------------------")

    print("=====================")
    exit()





@app.task(name='reboot_vm')
def reboot_vm(vm_name):
    ssl._create_default_https_context = ssl._create_unverified_context
    si = SmartConnect(host=VCENTER, user=VCENTERUSER, pwd=VCENTERPASSWD, port=443)
    vm = vmutils.get_vm_by_name(si ,vm_name)
    vm.RebootGuest()
    Disconnect(si)
    return {vm_name:'reboot'}







if __name__ == "__main__":
    virtual_machine_device_info('4201b88d-3a9e-d16b-84af-13fb83df2819')