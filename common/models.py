import datetime
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions


# Create your models here.
# 点击量统计
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

# 每日点击量统计
class ReadDetail(models.Model):
    created_date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# 获取某个模型实例的阅读数量
class GetReadNum():

    def get_read_num(self):
        content_type = ContentType.objects.get_for_model(self)
        try:
            read_num = ReadNum.objects.get(content_type=content_type, object_id=self.pk).read_num
        except exceptions.ObjectDoesNotExist:
            read_num = 0
        return read_num

    class Meta:
        abstract = True