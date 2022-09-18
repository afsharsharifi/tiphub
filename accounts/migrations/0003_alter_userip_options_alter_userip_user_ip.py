# Generated by Django 4.1 on 2022-09-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userip"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userip",
            options={
                "verbose_name": "IP کاربر",
                "verbose_name_plural": "IP های کاربران",
            },
        ),
        migrations.AlterField(
            model_name="userip",
            name="user_ip",
            field=models.GenericIPAddressField(verbose_name="IP کاربر"),
        ),
    ]
