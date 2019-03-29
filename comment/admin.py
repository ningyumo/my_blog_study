from django.contrib import admin
from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment_user', 'comment_time', 'content_object', 'top_parent', 'parent']