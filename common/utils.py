import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail


# 创建或获取某个对象的点击数
def get_object_read_num(object):
    content_type = ContentType.objects.get_for_model(object)
    ReadNum.objects.get_or_create(content_type=content_type,object_id=object.pk)
    ReadNum.objects.filter(content_type=content_type,object_id=object.pk)\
                    .update(read_num=F('read_num') + 1)
    ReadDetail.objects.get_or_create(content_type=content_type,
                        object_id=object.pk, created_date=timezone.now())
    ReadDetail.objects.filter(content_type=content_type,object_id=object.pk,
                    created_date=timezone.now()).update(read_num=F('read_num') + 1)



# 获取7日内每日阅读总量
def get_seven_read_num_total(content_type):
    time_now = timezone.now().date()
    read_num_total = []
    dates = []
    for i in range(7, -1, -1):
        date = time_now - datetime.timedelta(days=i)
        read_num_in_date = ReadDetail.objects.filter(content_type=content_type, 
                                                    created_date=date)\
                                            .aggregate(total=Sum('read_num'))
        read_num_total.append(read_num_in_date['total'] or 0)
        dates.append(date.strftime('%m/%d'))
    return read_num_total, dates


