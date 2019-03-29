from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'nick_name', 'email', 'is_staff', 'is_active', 'is_superuser']

    def nick_name(self, obj):
        return obj.profile.nick_name

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nick_name', 'user']