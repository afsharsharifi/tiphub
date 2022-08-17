from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('fullname', 'phone', 'email', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('fullname', 'email', 'image', 'biography')}),
        ('دسترسی ها', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fullname', 'phone', 'email', 'image', 'biography', 'password1', 'password2'),
        }),
    )
    search_fields = ('fullname', 'phone', 'email')
    ordering = ('fullname',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
