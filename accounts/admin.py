from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('fullname', 'phone', 'email', 'is_active', 'is_admin', 'otp_code')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('fullname', 'email', 'image')}),
        ('دسترسی ها', {'fields': ('is_admin', 'is_active', 'is_phone_verified', 'is_email_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fullname', 'phone', 'email', 'image', 'password1', 'password2'),
        }),
    )
    search_fields = ('fullname', 'phone', 'email')
    ordering = ('fullname',)
    filter_horizontal = ()


@admin.register(models.UserIP)
class UserIPAdmin(admin.ModelAdmin):
    list_display = ('user_ip',)


@admin.register(models.BlockUserIP)
class BlockUserIPAdmin(admin.ModelAdmin):
    list_display = ('blocked_ip',)


admin.site.unregister(Group)
