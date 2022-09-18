from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from extensions.utils import get_extension_file, username_from_email

from .managers import CustomUserManager


def create_image_path_user(instance, filename):
    extension = get_extension_file(filename)
    username = username_from_email(instance.email)
    return f"users/{username}{extension}"


class CustomUser(AbstractBaseUser):
    fullname = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    otp_code = models.CharField(max_length=6, null=True, verbose_name="کد یکبار مصرف", editable=False)
    is_phone_verified = models.BooleanField(default=False, verbose_name="تلفن تایید شده")
    email = models.EmailField(max_length=255, unique=True, verbose_name="ایمیل")
    is_email_verified = models.BooleanField(default=False, verbose_name="ایمیل تایید شده")
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


class UserIP(models.Model):
    user_ip = models.GenericIPAddressField(verbose_name="IP کاربر")

    class Meta:
        verbose_name = 'IP کاربر'
        verbose_name_plural = 'IP های کاربران'

    def __str__(self):
        return self.user_ip
