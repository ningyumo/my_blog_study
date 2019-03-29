from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from .models import LikeCount, LikeRecord


'''content_type: content_type,
object_id: object_id,
whether_like: whether_like,'''
# Create your views here.
def change_like(request):
    data = {}
    user = request.user
    if user.is_authenticated:
        content_type = request.GET.get('content_type')
        object_id = request.GET.get('object_id')
        try:
            content_type = ContentType.objects.get(model=content_type)
            model_class = content_type.model_class()
            object = model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            data['status'] = 'ERROR_NO_OBJECT'
            data['message'] = '点赞对象不存在'
            return JsonResponse(data)
        whether_like = request.GET.get('whether_like')
        if whether_like == 'true':
            # 要点赞
            like_count, created = LikeCount.objects.get_or_create(
                content_type=content_type, object_id=object_id)
            like_count.total_num += 1
            like_count.save()
            like_record, created = LikeRecord.objects.get_or_create(
                content_type=content_type, object_id=object_id, user = user)
            data['status'] = 'SUCCESS'
            data['total_num'] = like_count.total_num
            return JsonResponse(data)
        else:
            # 取消点赞
            like_count = LikeCount.objects.get(content_type=content_type,
                    object_id=object_id)
            like_count.total_num -= 1
            like_count.save()
            LikeRecord.objects.get(content_type=content_type, object_id=object_id,
                    user=user).delete()
            data['status'] = 'SUCCESS'
            data['total_num'] = like_count.total_num
            return JsonResponse(data)
    else:
        data['status'] = 'ERROR_NOT_LOGIN'
        data['message'] = "登录后方可点赞"
        return JsonResponse(data)
        # return redirect(reverse('login'))