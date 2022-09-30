from email.policy import default
from accounts.models import CustomUser
from django.db import models

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="کاربر")
    title = models.CharField(max_length=150, verbose_name="عنوان")
    link = models.URLField(verbose_name="لینک")
    is_for_all = models.BooleanField(default=False, verbose_name="ارسال برای همه")

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلانات"

    def __str__(self):
        return self.title
