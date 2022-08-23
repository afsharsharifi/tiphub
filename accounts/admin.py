from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import models


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('fullname', 'phone', 'email', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('fullname', 'email', 'image')}),
        ('دسترسی ها', {'fields': ('is_admin', 'is_active')}),
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


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
