from django.shortcuts import render, HttpResponse

from django.views.generic import ListView
from django.db.models import Q
from django.db.models import CharField, GenericIPAddressField
from vsa.genericviews import SuperuserRequiredMixin
from .models import *
from .forms import MacRegLogForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import ProcessFormView
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404


# Create your views here.

class IpMacList(SuperuserRequiredMixin, ListView):
    model = MacRegLog
    template_name = 'ipmaclist.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(IpMacList, self).get_context_data(**kwargs)
        context['count'] = dict(maccount=self.model.objects.all().count())
        # context['count'] = {'maccount':1666}
        return context

    def get_queryset(self):
        queryset = super(IpMacList,self).get_queryset()
        if 'q' in self.request.GET:
            q = self.request.GET.get('q')
            fields = [f for f in self.model._meta.fields if isinstance(f,CharField)|isinstance(f,GenericIPAddressField)]
            queries = [Q(**{f.name + "__contains":q}) for f in fields]
            qs = Q()
            for query in queries:
                qs = qs|query
            object = self.model.objects.filter(qs)
        else:
            object = self.model.objects.all()
        return object

    # def _allowed_methods(self):
    #     self.http_method_names.append("post")
    #     return [method.upper() for method in self.http_method_names if hasattr(self,method)]

    def dispatch(self, request, *args, **kwargs):
        self.http_method_names.append("post")
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class IPMacView(ContextMixin,View):
    template_name = 'ipmaclist.html'
    paginator_class = Paginator
    paginate_by = None

    def get(self,request,*args,**kwargs):
        self.authlog = MacRegLog.objects.all()
        return render(request,self.template_name,{'object_list':self.authlog})

    def get_paginate_by(self):
        """
        Get the number of items to paginate by, or ``10`` for default Search object pagination.
        """
        return self.paginate_by or 10

    def paginate_search_object(self, es_search_object, page_size):
        """
        Paginate the search_object.
        Note: Unlike QuerySet, you can not use es_queryset for pagination, but use Search object es_search_object
        Please refer to the manual of Search class
        """
        paginator = self.get_paginator(
            self.authlog, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page_obj = paginator.page(page_number)
            return (paginator, page_obj, page_obj.object_list, page_obj.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginator(self, authlog, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        """
        Return an instance of the paginator for this view.
        Object to be paginated should be Search object, not Response object of Search.execute()
        """
        return self.paginator_class(
            es_search_object, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty
    def post(self):
        pass




@csrf_exempt
def revinterface(request):

    record = {'authuser': request.POST.get('authuser'), 'ip': request.POST.get('ip'), 'mac': request.POST.get('mac'),
              'switch': request.POST.get('switch')}
    # print record
    log = MacRegLog.objects.create(**record)

    return HttpResponse(record)


def getmacreglogcount(request):
    return HttpResponse(MacRegLog.objects.all().count())



def test(request):
    salt = request.GET.get('salt')
    content = '''<!-- 156929ece43ebd6aabe538daf82e7ad3e1c545c120c29ccae8b7c96f73c05430861cbd764d2956c3cd2d7710357e8f4898d4c4e93ee5c11a686cc112af78803d -->\n<ObtainTicketResponse><message></message><prolongationPeriod>607875500</prolongationPeriod><responseCode>OK</responseCode><salt>%s</salt><ticketId>1</ticketId><ticketProperties>licensee=songtao\tlicenseType=0\t</ticketProperties></ObtainTicketResponse>''' %salt
    return HttpResponse(content,content_type='text/plain')
