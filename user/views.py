import string
import random
import time

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail

from .forms import LoginForm, RegForm, ChangeDisplayNameForm, ChangeEmailForm, ChangePasswordForm, ResetPasswordForm
from .models import Profile


def register(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = RegForm(request.POST, request=request)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            del request.session['register']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(redirect_to)
    else:
        form = RegForm()
    context = {}
    context['form'] = form
    return render(request, 'user/register.html', context)


def login(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth.login(request, user)
            return redirect(redirect_to)
    else:
        form = LoginForm()
    context = {}
    context['form'] = form
    return render(request, 'user/login.html', context)


def modal_login(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def logout(request):
    redirect_to = request.GET.get('from', reverse('home'))
    auth.logout(request)
    return redirect(redirect_to)


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def change_displayname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeDisplayNameForm(request.POST, user=request.user)
        if form.is_valid():
            displayname_new = form.cleaned_data['displayname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.displayname = displayname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeDisplayNameForm()
    context = {}
    context['page_title'] = "修改昵称"
    context['form_title'] = "修改昵称"
    context['submit_text'] = "修改"
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request, 'user/form.html', context)


def change_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            del request.session['change_email_vc']
            return redirect(redirect_to)
    else:
        form = ChangeEmailForm()
    context = {}
    context['page_title'] = "修改邮箱"
    context['form_title'] = "修改邮箱"
    context['submit_text'] = "修改"
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request, 'user/change_email.html', context)


def change_password(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request=request)
        if form.is_valid():
            user = request.user
            password_new = form.cleaned_data['password_new']
            user.set_password(password_new)
            user.save()
            auth.login(request,
                       auth.authenticate(request, username=request.user.username, password=request.user.password))
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = "修改密码"
    context['form_title'] = "修改密码"
    context['submit_text'] = "修改"
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request, 'user/form.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    purpose = request.GET.get('purpose', '')
    data = {}
    if email != '':
        verification_code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_time = request.session.get('send_time', 0)
        if now - send_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[purpose] = verification_code
            request.session['send_time'] = now

            # 发送验证码
            send_mail(
                '修改邮箱',
                '验证码：{}'.format(verification_code),
                'himen.akamon@gmail.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def reset_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password_new = form.cleaned_data['password_new']
            user = User.objects.get(email=email)
            user.set_password(password_new)
            user.save()
            del request.session['reset_password_vc']
            return redirect(redirect_to)
    else:
        form = ResetPasswordForm()
    context = {}
    context['page_title'] = "重置密码"
    context['form_title'] = "重置密码"
    context['submit_text'] = "重置"
    context['form'] = form
    context['redirect_to'] = redirect_to
    return render(request, 'user/reset_password.html', context)