from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentSubmitForm


# Create your views here.
def submit_comment(request):
    data = {}
    if request.method == 'POST':
        comment_submit_form = CommentSubmitForm(request.POST, user=request.user)
        if comment_submit_form.is_valid():
            comment_user = comment_submit_form.cleaned_data['user']
            text = comment_submit_form.cleaned_data['text']
            content_object = comment_submit_form.cleaned_data['content_object']
            parent = comment_submit_form.cleaned_data['parent']

            # 判断是不是一级评论
            if parent:
                # 不是一级评论
                comment = Comment.objects.create(comment_user=comment_user,
                    text=text,
                    content_object=content_object,
                    reply_to=parent.comment_user,
                    parent=parent,
                    top_parent=parent.top_parent if parent.top_parent else parent
                    )
                data['reply_to'] = comment.reply_to.username
                data['top_parent_pk'] = comment.top_parent.pk
            else:
                #是一级评论
                comment = Comment.objects.create(comment_user=comment_user,
                        text=text,
                        content_object=content_object,
                        reply_to=None,
                        parent=None,
                        top_parent=parent)
            # 返回数据
            data['status'] = 'SUCCESS'
            data['username'] = comment.comment_user.username
            data['comment_time'] = comment.comment_time.strftime("%Y-%m-%d %H:%M:%S")
            data['text'] = comment.text
            data['content_type'] = ContentType.objects.get_for_model(comment).model
            data['pk'] = comment.pk

        else:
            data['status'] = 'ERROR'
            data['message'] = list(comment_submit_form.errors.values())[0][0]
    return JsonResponse(data)  
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # return redirect(referer)


