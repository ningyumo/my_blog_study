import datetime
import string
import random
import time
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from common.utils import get_seven_read_num_total
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Sum
from blog.models import Blog
from common.utils import ReadDetail
from .forms import LoginForm, RegisterForm, ChangeNickNameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from user.models import Profile
from django.core.mail import send_mail


# 获取num天热门博客
def get_hot_data(num):
    content_type = ContentType.objects.get_for_model(Blog)
    time_now = timezone.now().date()
    time_ago = time_now - datetime.timedelta(days=num)
    hot_datas = ReadDetail.objects.filter(content_type=content_type,
                            created_date__gte=time_ago)\
                            .values('blog__title', 'blog__pk')\
                            .annotate(total_click=Sum('read_num'))\
                            .order_by('-total_click')[:10]
    return hot_datas


def home(request):
    content_type = ContentType.objects.get_for_model(Blog)
    read_num_total, date = get_seven_read_num_total(content_type)
    # 获取24小时热门博客
    # 下面是获取缓存的
    # hot_datas_24hours = cache.get_or_set('hot_datas_24hours',get_hot_data(1), 30)
    hot_datas_24hours = get_hot_data(1)

    # 获取7日热门博客
    # 下面是获取缓存的
    # hot_datas_week = cache.get_or_set('hot_datas_week',get_hot_data(7), 30)
    hot_datas_week = get_hot_data(7)

    # 获取30天热门博客
    # 下面是获取缓存的
    # hot_datas_month = cache.get_or_set('hot_datas_month',get_hot_data(30), 30)
    hot_datas_month = get_hot_data(30)

    context = {}
    context['read_num_total'] = read_num_total
    context['date'] = date
    context['hot_datas_24hours'] =hot_datas_24hours
    context['hot_datas_week'] =hot_datas_week
    context['hot_datas_month'] =hot_datas_month
    return render(request, 'home.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']

            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request=request)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            # 登录用户
            user =auth.authenticate(username=username, password=password) 
            auth.login(request, user)
            del request.session['register']
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'register.html', context)


def login_for_modal(request):
    if request.method == 'POST':
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
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request, user_pk):
    return render(request, 'user_info.html')


def change_nick_name(request):
    from_where = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNickNameForm(request.POST, user=request.user)
        if form.is_valid():
            nick_name = form.cleaned_data['nick_name']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nick_name = nick_name
            profile.save()
            return redirect(from_where)
    else:
        form = ChangeNickNameForm()
    context = {}
    context['form'] = form
    context['title'] = '修改昵称'
    context['from_where'] = from_where
    return render(request, 'change_form.html', context)


def bind_email(request):
    from_where = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email']
            return redirect(from_where)
    else:
        form = BindEmailForm()
    context = {}
    context['form'] = form
    context['title'] = '修改邮箱'
    context['from_where'] = from_where
    return render(request, 'bind_email.html', context)


def send_verify_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '' :
        # 生成验证码
        verify_code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session[send_for] = verify_code
        # 发送邮件
        send_mail(
            '绑定邮箱',
            '验证码：%s' % verify_code,
            '653056889@qq.com',
            [email],
            fail_silently=False,
            )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    from_where = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            auth.logout(request)
            return redirect(reverse('home'))
    else:
        form = ChangePasswordForm()
    context = {}
    context['form'] = form
    context['title'] = '修改密码'
    context['from_where'] = from_where
    return render(request, 'change_form.html', context)


def forgot_password(request):
    from_where = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            del request.session['forgot_password']
            return redirect(from_where)
    else:
        form = ForgotPasswordForm()
    context = {}
    context['form'] = form
    context['title'] = '找回密码'
    # context['from_where'] = from_where
    return render(request, 'forgot_password.html', context)
