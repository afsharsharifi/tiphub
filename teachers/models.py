from django.db import models
from accounts.models import CustomUser
from extensions.utils import get_extension_file, username_from_email
from django.urls import reverse


def create_resume_path_teacher(instance, filename):
    extension = get_extension_file(filename)
    username = username_from_email(instance.email)
    return f"teachers/{username}{extension}"


class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")
    username = models.CharField(max_length=250, unique=True, verbose_name="نام کاربری")
    title = models.CharField(max_length=250, null=True, blank=True, verbose_name="عنوان")
    about = models.TextField(null=True, blank=True, verbose_name="درباره")
    instagram = models.CharField(max_length=250, null=True, blank=True, verbose_name="اینستاگرام")
    twitter = models.CharField(max_length=250, null=True, blank=True, verbose_name="توییتر")
    github = models.CharField(max_length=250, null=True, blank=True, verbose_name="گیت هاب")
    gitlab = models.CharField(max_length=250, null=True, blank=True, verbose_name="گیت لب")
    linkedin = models.CharField(max_length=250, null=True, blank=True, verbose_name="لینکدین")
    telegram = models.CharField(max_length=250, null=True, blank=True, verbose_name="تلگرام")
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, verbose_name="ایمیل (پروفایل)")
    website = models.URLField(null=True, blank=True, verbose_name="وبسایت")
    resume = models.FileField(upload_to=create_resume_path_teacher, null=True, blank=True, verbose_name="فایل رزومه")

    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("teachers:teacher_detail", kwargs={"username": self.username})
