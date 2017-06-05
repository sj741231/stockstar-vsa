# -*- coding: utf-8 -*-
__author__ = 'songtao'

import pyVmomi
import argparse
import atexit
import itertools
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect, Disconnect
import ssl

from vsa.settings import VCENTERPASSWD,VCENTERUSER,VCENTER
ssl._create_default_https_context = ssl._create_unverified_context


MBFACTOR = float(1 << 20)

def printHostInformation(host):
    try:
        summary = host.summary
        stats = summary.quickStats
        hardware = host.hardware
        cpuUsage = stats.overallCpuUsage
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize/MBFACTOR
        memoryUsage = stats.overallMemoryUsage
        freeMemoryPercentage = 100 - (
            (float(memoryUsage) / memoryCapacityInMB) * 100
        )
        print "--------------------------------------------------"
        print "Host name: ", host.name
        print "Host CPU usage: ", cpuUsage
        # print "Host memory capacity: ", humanize.naturalsize(memoryCapacity,
        #                                                      binary=True)
        print "Host memory usage: ", memoryUsage / 1024, "GiB"
        print "Free memory percentage: " + str(freeMemoryPercentage) + "%"
        print "--------------------------------------------------"
    except Exception as error:
        print "Unable to access information for host: ", host.name
        print error
        pass

def printComputeResourceInformation(computeResource):
    try:
        hostList = computeResource.host
        print "##################################################"
        print "Compute resource name: ", computeResource.name
        print "##################################################"
        for host in hostList:
            printHostInformation(host)
    except Exception as error:
        print "Unable to access information for compute resource: ",
        computeResource.name
        print error
        pass

def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        si = SmartConnect(host=VCENTER, user=VCENTERUSER,pwd=VCENTERPASSWD,sslContext=ssl_context)
        atexit.register(Disconnect, si)
        content = si.RetrieveContent()

        for datacenter in content.rootFolder.childEntity:
            print "##################################################"
            print "##################################################"
            print "### datacenter : " + datacenter.name
            print "##################################################"

            if hasattr(datacenter.vmFolder, 'childEntity'):
                hostFolder = datacenter.hostFolder
                computeResourceList = hostFolder.childEntity
                for computeResource in computeResourceList:
                    printComputeResourceInformation(computeResource)

    except vmodl.MethodFault as error:
        print "Caught vmodl fault : " + error.msg
        return -1
    return 0

if __name__ == "__main__":
    main()