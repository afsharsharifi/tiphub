from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("show_image", "title", "teacher", "duration", "jalali_published_at", "jalali_updated_at")
    list_display_links = ("title",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "parent")


@admin.register(models.Like)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "jalali_liked_at")


@admin.register(models.Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("user", "video", "parent", "commented_at")
