from django.contrib import admin
from . import models
# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username')
    fieldsets = (
        (None, {'fields': ('user', 'username')}),
        ('اطلاعات شخصی', {'fields': ('title', 'about')}),
        ('شبکه های اجتماعی', {'fields': ('instagram', 'twitter', 'github', 'gitlab', 'linkedin', 'telegram', 'email', 'website')}),
        ('فایل رزومه', {'fields': ('resume',)}),
    )
    search_fields = ('user', 'username', 'email')


admin.site.register(models.Teacher, TeacherAdmin)
