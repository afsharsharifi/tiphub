from django.db import models
from accounts.models import CustomUser
from teachers.models import Teacher
from ckeditor.fields import RichTextField
from extensions.utils import get_extension_file, numeric_month_to_name
from django.utils.text import slugify
from django.utils.html import format_html
import jdatetime
from django.urls import reverse
import re
# Create your models here.


def create_videos_path(instance, filename):
    extension = get_extension_file(filename)
    return f"teachers/videos/{instance.title}{extension}"


def create_cover_image_path(instance, filename):
    extension = get_extension_file(filename)
    return f"teachers/videos/covers/{instance.title}{extension}"


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان")
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, verbose_name="عنوان برای URL")
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.CASCADE, verbose_name="زیر دسته بندی")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.title

    def save(self):
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", self.slug):
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save()


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="videos", verbose_name="استاد")
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, verbose_name="عنوان برای URL")
    views = models.IntegerField(default=0, verbose_name="بازدیدها")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="videos", verbose_name="دسته بندی")
    video = models.FileField(upload_to=create_videos_path, verbose_name="فایل ویدئو")
    cover_image = models.ImageField(upload_to=create_cover_image_path, null=True, blank=True, verbose_name="کاور ویدئو")
    duration = models.DurationField(verbose_name="طول ویدئو")
    description = RichTextField(verbose_name="توضیحات")
    published_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئو ها"

    def __str__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save()

    def get_absolute_url(self):
        return reverse("videos:video_detail_view", kwargs={"slug": self.slug})

    def get_description(self):
        return format_html(self.description)

    def show_image(self):
        if self.cover_image:
            return format_html(f'<img src="{self.cover_image.url}" alt="{self.title}" width="30px">')
        return format_html("کاور ندارد")
    show_image.short_description = "تصویر کاور"

    def jalali_published_at(self):
        jalili_date = jdatetime.date.fromgregorian(date=self.published_at)
        return f"{jalili_date.day} {numeric_month_to_name(jalili_date.month)} {jalili_date.year}"
    jalali_published_at.short_description = "انتشار"

    def jalali_updated_at(self):
        jalili_date = jdatetime.date.fromgregorian(date=self.updated_at)
        return f"{jalili_date.day} {numeric_month_to_name(jalili_date.month)} {jalili_date.year}"
    jalali_updated_at.short_description = "بروزرسانی"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes", verbose_name="کاربر")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes", verbose_name="ویدئو")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"

    def __str__(self):
        return f"{self.user.fullname} - {self.video.title}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments", verbose_name="کاربر")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments", verbose_name="ویدئو")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", verbose_name="پاسخ به", null=True, blank=True)
    comment = models.TextField(verbose_name="کامنت")
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.user.fullname} - {self.video.title}"
