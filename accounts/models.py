import os
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import CustomUserManager


def username_from_email(email):
    return email.split("@")[0]


def get_extension_file(filename):
    return os.path.splitext(filename)[-1]


def create_image_path_user(instance, filename):
    extension = get_extension_file(filename)
    username = username_from_email(instance.email)
    return f"users/{username}{extension}"


def create_resume_path_teacher(instance, filename):
    extension = get_extension_file(filename)
    username = username_from_email(instance.email)
    return f"teachers/{username}{extension}"


class CustomUser(AbstractBaseUser):
    fullname = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    email = models.EmailField(max_length=255, unique=True, verbose_name="ایمیل")
    image = models.ImageField(upload_to=create_image_path_user, null=True, blank=True, verbose_name="تصویر پروفایل")
    joined = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="مدیر")

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['fullname', 'email']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


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
