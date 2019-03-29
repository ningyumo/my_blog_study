from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentSubmitForm


register = template.Library()



@register.simple_tag
def get_comments_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, 
            object_id=obj.pk).count()


@register.simple_tag
def get_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, 
                        object_id=obj.pk, parent=None).order_by('-comment_time')
    return comments


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_submit_form =  CommentSubmitForm(
                                initial={
                                    'content_type':content_type,
                                    'object_id': obj.pk,
                                    'reply_comment_id': 0,
                                })
    return comment_submit_form