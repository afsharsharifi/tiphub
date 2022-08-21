# Generated by Django 4.1 on 2022-08-21 13:56

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacher",
            name="about",
            field=models.TextField(blank=True, null=True, verbose_name="درباره"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="ایمیل (پروفایل)",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="github",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="گیت هاب"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="gitlab",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="گیت لب"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="instagram",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="اینستاگرام"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="linkedin",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="لینکدین"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="resume",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=accounts.models.create_resume_path_teacher,
                verbose_name="فایل رزومه",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="telegram",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="تلگرام"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="title",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="عنوان"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="twitter",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="توییتر"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="کاربر",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="username",
            field=models.CharField(
                max_length=250, unique=True, verbose_name="نام کاربری"
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="website",
            field=models.URLField(blank=True, null=True, verbose_name="وبسایت"),
        ),
    ]
