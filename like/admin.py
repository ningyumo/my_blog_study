from django.contrib import admin
from .models import LikeCount, LikeRecord


# Register your models here.
@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['total_num', 'content_object']


@admin.register(LikeRecord)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_object', 'liked_time']