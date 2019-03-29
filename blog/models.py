from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from common.models import GetReadNum, ReadDetail



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, GetReadNum):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    read_detail = GenericRelation(ReadDetail, related_query_name='blog')


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
