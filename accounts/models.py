import os
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


def username_from_email(email):
    return email.split("@")[0]


def get_extension_file(filename):
    return os.path.splitext(filename)[-1]


def create_image_path(instance, filename):
    extension = get_extension_file(filename)
    username = username_from_email(instance.email)
    return f"teachers/{username}{extension}"


class CustomUser(AbstractBaseUser):
    fullname = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    email = models.EmailField(max_length=255, unique=True, verbose_name="ایمیل")
    biography = models.TextField(null=True, blank=True, verbose_name="بیوگرافی")
    image = models.ImageField(upload_to=create_image_path, null=True, blank=True, verbose_name="تصویر پروفایل")
    joined = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="مدیر")

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['fullname', 'email']

    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'حساب ها'

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
