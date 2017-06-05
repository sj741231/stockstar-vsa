# -*-coding=utf8-*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext, loader
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, DeleteView, View, FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from forms import RegisterForm, LoginForm, UserForm, ChangePasswordForm
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
import arrow
from server.models import HostGroup, Host,Event



def index(request):
    """
    user login or not?
    if login return startpage
    else return login page
    """
    now = arrow.now()
    timeline =[]
    event_count = []
    if request.user.is_authenticated():
        for i in range(0,30):
            date = now.replace(days=-i)
            timeline.append(date.strftime('%Y-%m-%d'))
            count1 = Event.objects.filter(timestamp__range=(date.floor('day').datetime,date.ceil('day').datetime)).count()
            event_count.append(count1)

        return render(request,'index.html',locals())
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def login_view(request):
    error = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/')
        else:
            error = True
            return render_to_response('login.html', {'error': error})
    return render_to_response('login.html')


def register(request):
    ''''''
    template_var = {}
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST.copy())
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username, email, password)
            user.save()
            _login(request, username, password)
            return HttpResponseRedirect(reverse("index"))
    template_var["form"] = form
    return render_to_response("register.html", template_var, context_instance=RequestContext(request))


@csrf_exempt
@login_required()
def change_pass(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render_to_response('change_pass.html', {'form': form, 'username': request.user.username},
                              context_instance=RequestContext(request))


def myprofile(request):
    """
    user login or not?
    if login return startpage
    else return login page
    """
    if request.user.is_authenticated():
        username = request.user.username
        style = 'home'
        return render_to_response("myprofile.html", {'username': username, 'index': style},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))


def _login(request, username, password):
    ret = False
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth_login(request, user)
            ret = True
        else:
            messages.add_message(request, messages.INFO, _(u'User is not active'))
    else:
        messages.add_message(request, messages.INFO, _(u'error'))
    return ret


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


import json


def user_count(request):
    data = json.dumps({'project': User.objects.all().count()})
    return HttpResponse(data)


class adminchangepasword(FormView):
    form_class = AdminPasswordChangeForm
    template_name = 'adminchangeuserpassword.html'


def send_mail(self, subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()


def adminresetuserpassword(request, pk):
    user = get_object_or_404(User, pk=int(pk))
    email = user.email
    subject = u'重置运维平台密码--%s' % user.username
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    password_reset_url = 'http://%s/accounts/reset/%s/%s' % (request.get_host(), token, uid)
    mail_msg = u"""
    证金99运维平台--密码重置通知
    用户名：%s
    请点击链接:%s
    链接有效次数为1

    """ % (user.username, password_reset_url)
    email = EmailMessage(subject, mail_msg, to=[email])
    mail_status = email.send()
    if mail_status:
        return HttpResponse("<script> alert('" + u'密码重置邮件已发出' + "');window.location.href='/accounts/userlist'</script>")

        # return HttpResponse('<script> alert('" + u'密码重置邮件已发出' + "');</script>')
    return HttpResponse('<script> alert('" + u'密码重置邮件发送失败，请联系管理员:' + "')</script>')



    # domain_override=None
    # subject_template_name='registration/password_reset_subject.txt'
    # email_template_name='registration/password_reset_email.html'
    # use_https=False
    # token_generator=default_token_generator
    # from_email=None
    # request=None
    # html_email_template_name=None
    # extra_email_context=None
    #
    #
    #
    # current_site = get_current_site(request)
    # site_name = current_site.name
    # domain = current_site.domain
    # site_name = domain = domain_override
    # context = {
    #     'email': user.email,
    #     'domain': domain,
    #     'site_name': site_name,
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'user': user,
    #     'token': token_generator.make_token(user),
    #     'protocol': 'https' if use_https else 'http',
    # }
    # if extra_email_context is not None:
    #     context.update(extra_email_context)
    # send_mail(subject_template_name, email_template_name,
    #                context, from_email, user.email,
    #                html_email_template_name=html_email_template_name)

from tasks import add_user

@login_required()
def send_pk(request,pk):
    u = get_object_or_404(User,pk=pk)
    print u.username,u.email
    result = add_user.delay(u.username,u.email)
    return HttpResponse("<script> alert('" + u'密钥已发送:' + "');window.location.href='/accounts/userlist'</script>")