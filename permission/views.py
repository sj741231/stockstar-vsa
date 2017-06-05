# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import ModelFormMixin, FormMixin, DeleteView, UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from vsa.genericviews import *
from .models import *
from .forms import *

from .models import User_Host
from .tasks import *
from django.contrib.auth.decorators import login_required
from .forms import *
from vsa.genericviews import GenericUpdateView


# Create your views here.


def user_add_perm(request):
    form = PermForm()
    if request.method == "POST":
        form = PermForm(request)
        return render(request, 'user_add_perm.html', locals())
    return render(request, 'user_add_perm.html', locals())


@login_required()
def operate_user_perm(request, pk):
    perm = get_object_or_404(User_Host, pk=pk)
    username = perm.user.username
    for host in list_user_hosts(perm_id=perm.id):
        add_perm.delay(username=username, ip=host)
    return HttpResponse("<script> alert('" + u'主机授权中!' + "');window.location.href='/permission/perm'</script>")


@login_required()
def user_perm_info(request, pk):
    user_perm = get_object_or_404(User_Host, pk=pk)
    return render(request, 'users_perm.html', locals())


@login_required()
def refresh_user_perm(request, pk):
    perm = get_object_or_404(User_Host, pk=pk)
    x = refresh_key.delay(perm.id)
    return HttpResponse("<script> alert('" + u'授权刷新中!' + "');window.location.href='/permission/perm'</script>")


@login_required()
def refresh_host_key(request, pk):
    perm = get_object_or_404(User_Host, pk=pk)
    username = perm.user.username
    for host in list_user_hosts(perm_id=perm.id):
        SyncKey.delay(username=username, ip=host)
    return HttpResponse("<script> alert('" + u'授权刷新中!' + "');window.location.href='/permission/perm'</script>")


class userpermupdateview(GenericUpdateView):
    template_name = 'userpermupdate.html'

    def post(self, request, *args, **kwargs):
        perm = request.POST.get()


@login_required()
def multadduserperm(request):
    '''
    多用户，多机器同时授权
    :param request:
    :return:
    '''
    form = MuitiAddPerm()
    if request.method == 'POST':
        form = MuitiAddPerm(request.POST)
        if form.is_valid():
            hostlist = Host.objects.filter(pk__in=request.POST.getlist('hosts'))
            for userid in request.POST.getlist('userlist'):
                perm, status = User_Host.objects.get_or_create(user_id=userid)
                for h in hostlist:
                    perm.host.add(h)
                    add_perm.delay(username=perm.user.username, ip=h.ip)
            return HttpResponse("<script> alert('" + u'批量授权中!' + "');window.location.href='/permission/perm'</script>")
    return render(request, 'multadduserperm.html', locals())


class UserPermIndexView(ListView):
    model = User
    template_name = 'userpermindex.html'

    # def get_context_data(self, **kwargs):
    #     context = super(UserPermIndexView,self).get_context_data(**kwargs)
    #     return  context


class UserPermListView(ListView):
    model = UserPerm
    template_name = 'userpermlist.html'

    def get_context_data(self, **kwargs):
        context = super(UserPermListView, self).get_context_data(**kwargs)
        userid = self.kwargs.get('userid', None)
        if userid:
            self.user = User.objects.get(id=userid)
            context['user'] = self.user
        return context

    def get_queryset(self):
        user_id = self.kwargs.get('userid', None)
        if user_id:
            queryset = self.model.objects.filter(user_id=self.kwargs['userid'])
        else:
            queryset = self.model.objects.all()
        return queryset


def remote_add_perm(request, pk):
    perm = get_object_or_404(UserPerm, pk=pk)
    add_perm.delay(perm.user.username, perm.host.ip)
    return HttpResponse("<script> alert('" + u'授权中!' + "');window.location.href=''</script>")


class PermCreateView(SuperuserRequiredMixin, CreateView):
    # model = Records
    form_class = UserPermForm
    template_name = 'userpermform.html'
    success_url = reverse_lazy('userpermlist')

    def get_initial(self):
        userid = self.kwargs.get('userid', None)
        if userid:
            self.user = get_object_or_404(UserPerm, pk=userid)
            return {'user': self.user}

    def get_context_data(self, **kwargs):
        context = super(PermCreateView, self).get_context_data(**kwargs)
        context['zone'] = self.user
        context['success_url'] = reverse('userpermlist', kwargs={'pk': self.user.id})

        return context

    def get_success_url(self):
        return reverse_lazy('userpermlist', kwargs={'pk': self.user.id})


@login_required()
def add_permission(request):
    '''
    多用户，多机器同时授权
    :param request:
    :return:
    '''
    form = UserPermform1()
    if request.method == 'POST':
        form = UserPermform1(request.POST)
        if form.is_valid():
            hostlist = virtualhost.objects.filter(pk__in=request.POST.getlist('hosts'))
            for userid in request.POST.getlist('userlist'):
                for h in hostlist:
                    perm, status = UserPerm.objects.get_or_create(user_id=userid, host=h)
                    add_perm.delay(username=perm.user.username, ip=h.ip)

            return HttpResponse("<script> alert('" + '授权中!' + "');window.location.href='/permission/index'</script>")
    return render(request, 'multadduserperm.html', locals())



def multi_add_permission(request):
    pass