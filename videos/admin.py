from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("show_image", "title", "teacher", "views", "duration", "jalali_published_at", "jalali_updated_at")
    list_display_links = ("title",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "parent")
