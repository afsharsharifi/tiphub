# Generated by Django 4.1 on 2022-09-18 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_userip_options_alter_userip_user_ip"),
        ("videos", "0003_remove_video_views_video_viewers_by_ip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="viewers_by_ip",
            field=models.ManyToManyField(
                blank=True,
                default="192.168.0.1",
                related_name="viewer",
                to="accounts.userip",
                verbose_name="بازدیدکنندگان بر اساس IP",
            ),
        ),
    ]
