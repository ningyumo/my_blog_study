from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



# Create your models here.
class Comment(models.Model):
    comment_user = models.ForeignKey(User, 
        on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    reply_to = models.ForeignKey(User, on_delete=models.CASCADE,
        null=True, blank=True, related_name='replies',)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
        null=True, blank=True, related_name='child_comments')
    top_parent = models.ForeignKey('self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='progeny_comments')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  