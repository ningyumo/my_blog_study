from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog, BlogType
from common.utils import get_object_read_num
from comment.models import Comment
from comment.forms import CommentSubmitForm
from myboke.forms import LoginForm

# Create your views here.
# 分页
def my_paginator(request, query_set, num_per_page=5):
    # 创建分页
    paginator = Paginator(query_set, num_per_page)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    # 显示页码
    current_page_num = page.number
    if paginator.num_pages < 7:
        page_range = paginator.page_range
    else:
        if current_page_num < 5:
            page_range = range(1,8)
        elif 5 <= current_page_num <= paginator.num_pages - 3:
            page_range = range(current_page_num - 3, current_page_num + 4)
        elif current_page_num > paginator.num_pages - 3:
            page_range = range(paginator.num_pages - 6, paginator.num_pages + 1)
    context = {}
    context['page'] = page
    context['page_range'] = page_range
    return context


# 各列表共同部分
def common_list(request, query_set):
    # 获取博客发表时间
    blog_dates = query_set.dates("created_time", "month")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blogs_total_date = Blog.objects.filter(created_time__year=blog_date.year,
                                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blogs_total_date

    # 获取每种分类博客的数量
    blog_types = BlogType.objects.annotate(blogs_total_type=Count('blog'))
    # 获取分页信息
    context = my_paginator(request, query_set)
    context['blog_types'] = blog_types
    context['blog_dates'] = blog_dates_dict
    return context
    

# 博客列表
def blog_list(request):
    blog = Blog.objects.filter(is_delete=False)
    
    # 获取公共部分context
    context = common_list(request, blog)
    '''context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = blog_dates'''
    return render(request, "blog/blog_list.html", context)


# 博客内容
def blog_detail(request, blog_pk):
    # 获取本篇博客内容以及上下两篇博客
    blog = get_object_or_404(Blog, pk=blog_pk)
    previous_blog = Blog.objects.filter(pk__gt=blog.pk).last()
    next_blog = Blog.objects.filter(pk__lt=blog.pk).first()

    # 如果COOKIE不存在，则获取博客阅读数量
    # if not request.COOKIES.get('blog_%s_read' % blog.pk, None):
    get_object_read_num(blog)

    context = {}
    context["blog"] = blog
    context["previous_blog"] = previous_blog
    context["next_blog"] = next_blog
    context['login_form'] = LoginForm()

    response = render(request, "blog/blog_detail.html", context)
    # response.set_cookie('blog_%s_read' % blog.pk, 'True', max_age=60)
    return response


# 按类型分类列表
def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog = Blog.objects.filter(blog_type=blog_type)
    
    # 获取公共部分context
    context = common_list(request, blog)
    '''
    由于按类型分类时，传入的blog是本类型的blog列表，所以需要改写contex['blog_dates']
    需要传入所有blog列表。
    '''
    blog_dates = Blog.objects.filter(is_delete=False).dates("created_time", "month")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blogs_total_date = Blog.objects.filter(created_time__year=blog_date.year,
                                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blogs_total_date
    context['blog_dates'] = blog_dates_dict
    context["blog_type"] = blog_type
    return render(request, "blog/blogs_with_type.html", context)


# 按时间分类列表
def blogs_with_date(request, year, month):
    blog = Blog.objects.filter(created_time__year=year, created_time__month=month)
    
    # 获取公共部分context
    context = common_list(request, blog)
    context['date'] = "%s年%s月" % (year, month)
    return render(request, "blog/blogs_with_date.html", context)