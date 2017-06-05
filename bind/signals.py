from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Domain,Records


@receiver(post_save,sender = Domain)
def initial_record(sender,**kwargs):
    domain = Domain.objects.get(domain=kwargs['instance'])
    ns_data = 'ns1' + domain.domain
    primay_ns = ns_data +'.'
    ns_a = {'zone':domain,'host':'ns1','type':'A','data':settings.BINDSERVERADDR,'primary_ns':''}
    ns = {'zone':domain,'host':'','type':'NS','data':ns_data,'primary_ns':''}
    soa = {'zone':domain,'host':'@','type':'SOA','data':ns_data,'primary_ns':primay_ns}
    Records.objects.create(**ns_a)
    Records.objects.create(**ns)
    Records.objects.create(**soa)





