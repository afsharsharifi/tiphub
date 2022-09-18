from django.contrib import admin

from . import models


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username')
    fieldsets = (
        (None, {'fields': ('user', 'username')}),
        ('اطلاعات شخصی', {'fields': ('title', 'about')}),
        ('شبکه های اجتماعی', {'fields': ('instagram', 'twitter', 'github', 'gitlab', 'linkedin', 'telegram', 'email', 'website')}),
        ('فایل رزومه', {'fields': ('resume',)}),
    )
    search_fields = ('user', 'username', 'email')
