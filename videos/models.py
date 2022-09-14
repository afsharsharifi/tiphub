from django.db import models
from teachers.models import Teacher
from ckeditor.fields import RichTextField
from extensions.utils import get_extension_file
from django.utils.text import slugify
from django.utils.html import format_html
import jdatetime
# Create your models here.


def create_videos_path(instance, filename):
    extension = get_extension_file(filename)
    return f"teachers/videos/{instance.title}{extension}"


def create_cover_image_path(instance, filename):
    extension = get_extension_file(filename)
    return f"teachers/videos/covers/{instance.title}{extension}"


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان")
    url = models.CharField(max_length=100, unique=True, verbose_name="عنوان برای URL")
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.CASCADE, verbose_name="والد")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="videos", verbose_name="استاد")
    slug = models.SlugField(unique=True, editable=False)
    views = models.IntegerField(default=0, verbose_name="بازدیدها")
    video = models.FileField(upload_to=create_videos_path, verbose_name="فایل ویدئو")
    cover_image = models.ImageField(upload_to=create_cover_image_path, null=True, blank=True, verbose_name="کاور ویدئو")
    duration = models.DurationField(verbose_name="طول ویدئو")
    description = RichTextField(verbose_name="توضیحات")
    published_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئو ها"

    def show_image(self):
        if self.cover_image:
            return format_html(f'<img src="{self.cover_image.url}" alt="{self.title}" width="30px">')
        return format_html("کاور ندارد")
    show_image.short_description = "تصویر کاور"

    def jalali_published_at(self):
        jalili_date = jdatetime.date.fromgregorian(date=self.published_at)
        return jalili_date
    jalali_published_at.short_description = "انتشار"

    def jalali_updated_at(self):
        jalili_date = jdatetime.date.fromgregorian(date=self.updated_at)
        return jalili_date
    jalali_updated_at.short_description = "بروزرسانی"
