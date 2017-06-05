__author__ = 'songtao'
# -*- coding: utf-8 -*-


import hashlib
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from resources.models import *


def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

# def selfip_notuse_all(category,):
#     ip_in_list = IpAddress.objects.filter(
#         Q(id=self.instance.ip_in_id) |
#         Q(category='inside', inuse=False)
#     )
#     ip_in_field = self.fields['ip_in'].widget
#     ip_in_choices = []
#     ip_in_choices.append(('', '------'))
#     for ip_in in ip_in_list:
#         ip_in_choices.append((ip_in.id, ip_in.address))
#         ip_in_field.choices = ip_in_choices


def update_ip_use_status(ip, inuse):
    from .models import IpAddress
    IpAddress.objects.filter(address=ip).update(inuse=inuse)


def update_rack_is_inuse_status(rack_pos_id, is_inuse):
    from .models import RackPosition
    RackPosition.objects.filter(id=rack_pos_id).update(is_inuse=is_inuse)


def check_ip_inuse_change(self, ip_orig, ip_now):
    update_to_inuse = ''
    update_to_not_inuse = ''
    if ip_orig != ip_now:
        if ip_orig is None and ip_now:
            update_ip_use_status(ip_now, True)
        if ip_orig and ip_now is None:
            update_ip_use_status(ip_orig, False)
        if ip_orig and ip_now:
            update_ip_use_status(ip_now, True)
            update_ip_use_status(ip_orig, False)


def host_save(self, *args, **kwargs):
    from .models import Host
    from idc.models import Ipaddress
    if self.phy_host:
        phy_host_is_set = True
    else:
        phy_host_is_set = False
    if self.is_virtual ^ phy_host_is_set:
        raise IntegrityError("If this is a virtual host, "
                             "you need select a parent physical host,"
                             "otherwise, you need not.")
    #
    # if current instance has exist in db
    #
    if self.pk:
        host = Host.objects.get(pk=self.pk)
        #
        # if current instance has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current self properties, and then
        # change current instance's properties: ip_in, ip_out, ip_man
        # if current instance has all properties: rack_pos_start, rack_pos_end
        # and different from the three current self properties, and then
        # change current instance's properties: rack_pos_start, rack_pos_end
        #
        if host.ip_in and host.ip_in != self.ip_in:
            ip = host.ip_in.address
            update_ip_use_status(Ipaddress, False)
        if host.ip_out and host.ip_out != self.ip_out:
            ip = host.ip_out.address
            update_ip_use_status(Ipaddress, False)
        if host.ip_man and host.ip_man != self.ip_man:
            ip = host.ip_man.address
            update_ip_use_status(Ipaddress, False)
        if host.rack_pos_start and host.rack_pos_start != self.rack_pos_start:
            rack_pos_id = host.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        if host.rack_pos_end and host.rack_pos_end != self.rack_pos_end:
            rack_pos_id = host.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        #
        # if current self has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current instance's properties, and then
        # change current self's properties: ip_in, ip_out, ip_man
        # if current self has all properties: rack_pos_start, rack_pos_end
        # and different from the three current instance's properties, and then
        # change current self's properties: rack_pos_start, rack_pos_end
        #
        if self.ip_in and self.ip_in != host.ip_in:
            ip = self.ip_in.address
            update_ip_use_status(Ipaddress, True)
        if self.ip_out and self.ip_out != host.ip_out:
            ip = self.ip_out.address
            update_ip_use_status(Ipaddress, True)
        if self.ip_man and self.ip_man != host.ip_man:
            ip = self.ip_man.address
            update_ip_use_status(Ipaddress, True)
        if self.rack_pos_start and self.rack_pos_start != host.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end and self.rack_pos_end != host.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    #
    # if current self hasnot exist in db
    #
    else:
        if self.ip_in:
            ip = self.ip_in.address
            IpAddress.objects.filter(address=Ipaddress).update(inuse=True)
        if self.ip_out:
            ip = self.ip_out.address
            IpAddress.objects.filter(address=Ipaddress).update(inuse=True)
        if self.ip_man:
            ip = self.ip_man.address
            IpAddress.objects.filter(address=Ipaddress).update(inuse=True)
        if self.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    super(Host, self).save(*args, **kwargs)

def host_clean(self):
    if self.phy_host:
        phy_host_is_set = True
    else:
        phy_host_is_set = False
    if self.is_virtual != phy_host_is_set:
        raise ValidationError("If this is a virtual host, "
                             "you need select a parent physical host,"
                             "otherwise, you need not. %s %s")

def connection_clean(self):
    from .models import Connection
    #
    # if current intf1 has exist in db
    #
    intf1_type = self.intf1_type
    intf1_id = self.intf1_id
    intf1_is_exist = Connection.objects.filter(intf1_type=intf1_type, intf1_id=intf1_id)
    intf2_type = self.intf2_type
    intf2_id = self.intf2_id
    intf2_is_exist = Connection.objects.filter(intf2_type=intf2_type, intf2_id=intf2_id)

    if intf1_is_exist:
        raise ValidationError("Intf1 exists!")
    if intf2_is_exist:
        raise ValidationError("Intf2 exists!")


def switch_save(self, *args, **kwargs):
    from .models import Switch, IpAddress, RackPosition
    #
    # if current instance has exist in db
    #
    if self.pk:
        switch = Switch.objects.get(pk=self.pk)
        #
        # if current instance has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current self properties, and then
        # change current instance's properties: ip_in, ip_out, ip_man
        # if current instance has all properties: rack_pos_start, rack_pos_end
        # and different from the three current self properties, and then
        # change current instance's properties: rack_pos_start, rack_pos_end
        #
        if switch.ip and switch.ip != self.ip:
            ip = switch.ip.address
            update_ip_use_status(ip, False)
        if switch.rack_pos_start and switch.rack_pos_start != self.rack_pos_start:
            rack_pos_id = switch.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        if switch.rack_pos_end and switch.rack_pos_end != self.rack_pos_end:
            rack_pos_id = switch.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        #
        # if current self has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current instance's properties, and then
        # change current self's properties: ip_in, ip_out, ip_man
        # if current self has all properties: rack_pos_start, rack_pos_end
        # and different from the three current instance's properties, and then
        # change current self's properties: rack_pos_start, rack_pos_end
        #
        if self.ip and self.ip != switch.ip:
            ip = self.ip.address
            update_ip_use_status(ip, True)
        if self.rack_pos_start and self.rack_pos_start != switch.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end and self.rack_pos_end != switch.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    #
    # if current self hasnot exist in db
    #
    else:
        if self.ip:
            ip = self.ip.address
            IpAddress.objects.filter(address=ip).update(inuse=True)
        if self.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    super(Switch, self).save(*args, **kwargs)


def router_save(self, *args, **kwargs):
    from .models import Router, IpAddress, RackPosition
    #
    # if current instance has exist in db
    #
    if self.pk:
        router = Router.objects.get(pk=self.pk)
        #
        # if current instance has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current self properties, and then
        # change current instance's properties: ip_in, ip_out, ip_man
        # if current instance has all properties: rack_pos_start, rack_pos_end
        # and different from the three current self properties, and then
        # change current instance's properties: rack_pos_start, rack_pos_end
        #
        if router.ip and router.ip != self.ip:
            ip = router.ip.address
            update_ip_use_status(ip, False)
        if router.rack_pos_start and router.rack_pos_start != self.rack_pos_start:
            rack_pos_id = router.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        if router.rack_pos_end and router.rack_pos_end != self.rack_pos_end:
            rack_pos_id = router.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        #
        # if current self has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current instance's properties, and then
        # change current self's properties: ip_in, ip_out, ip_man
        # if current self has all properties: rack_pos_start, rack_pos_end
        # and different from the three current instance's properties, and then
        # change current self's properties: rack_pos_start, rack_pos_end
        #
        if self.ip and self.ip != router.ip:
            ip = self.ip.address
            update_ip_use_status(ip, True)
        if self.rack_pos_start and self.rack_pos_start != router.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end and self.rack_pos_end != router.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    #
    # if current self hasnot exist in db
    #
    else:
        if self.ip:
            ip = self.ip.address
            IpAddress.objects.filter(address=ip).update(inuse=True)
        if self.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    super(Router, self).save(*args, **kwargs)


def f5_save(self, *args, **kwargs):
    from .models import F5, IpAddress, RackPosition
    #
    # if current instance has exist in db
    #
    if self.pk:
        f5 = F5.objects.get(pk=self.pk)
        #
        # if current instance has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current self properties, and then
        # change current instance's properties: ip_in, ip_out, ip_man
        # if current instance has all properties: rack_pos_start, rack_pos_end
        # and different from the three current self properties, and then
        # change current instance's properties: rack_pos_start, rack_pos_end
        #
        if f5.ip and f5.ip != self.ip:
            ip = f5.ip.address
            update_ip_use_status(ip, False)
        if f5.rack_pos_start and f5.rack_pos_start != self.rack_pos_start:
            rack_pos_id = f5.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        if f5.rack_pos_end and f5.rack_pos_end != self.rack_pos_end:
            rack_pos_id = f5.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        #
        # if current self has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current instance's properties, and then
        # change current self's properties: ip_in, ip_out, ip_man
        # if current self has all properties: rack_pos_start, rack_pos_end
        # and different from the three current instance's properties, and then
        # change current self's properties: rack_pos_start, rack_pos_end
        #
        if self.ip and self.ip != f5.ip:
            ip = self.ip.address
            update_ip_use_status(ip, True)
        if self.rack_pos_start and self.rack_pos_start != f5.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end and self.rack_pos_end != f5.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    #
    # if current self hasnot exist in db
    #
    else:
        if self.ip:
            ip = self.ip.address
            IpAddress.objects.filter(address=ip).update(inuse=True)
        if self.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    super(F5, self).save(*args, **kwargs)


def firewall_save(self, *args, **kwargs):
    from .models import FireWall, IpAddress, RackPosition
    #
    # if current instance has exist in db
    #
    if self.pk:
        firewall = FireWall.objects.get(pk=self.pk)
        #
        # if current instance has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current self properties, and then
        # change current instance's properties: ip_in, ip_out, ip_man
        # if current instance has all properties: rack_pos_start, rack_pos_end
        # and different from the three current self properties, and then
        # change current instance's properties: rack_pos_start, rack_pos_end
        #
        if firewall.ip and firewall.ip != self.ip:
            ip = firewall.ip.address
            update_ip_use_status(ip, False)
        if firewall.rack_pos_start and firewall.rack_pos_start != self.rack_pos_start:
            rack_pos_id = firewall.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        if firewall.rack_pos_end and firewall.rack_pos_end != self.rack_pos_end:
            rack_pos_id = firewall.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=False
            )
        #
        # if current self has three all properties: ip_in, ip_out, ip_man,
        # and different from the three current instance's properties, and then
        # change current self's properties: ip_in, ip_out, ip_man
        # if current self has all properties: rack_pos_start, rack_pos_end
        # and different from the three current instance's properties, and then
        # change current self's properties: rack_pos_start, rack_pos_end
        #
        if self.ip and self.ip != firewall.ip:
            ip = self.ip.address
            update_ip_use_status(ip, True)
        if self.rack_pos_start and self.rack_pos_start != firewall.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end and self.rack_pos_end != firewall.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    #
    # if current self hasnot exist in db
    #
    else:
        if self.ip:
            ip = self.ip.address
            IpAddress.objects.filter(address=ip).update(inuse=True)
        if self.rack_pos_start:
            rack_pos_id = self.rack_pos_start_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
        if self.rack_pos_end:
            rack_pos_id = self.rack_pos_end_id
            update_rack_is_inuse_status(
                rack_pos_id=rack_pos_id,
                is_inuse=True
            )
    super(FireWall, self).save(*args, **kwargs)



