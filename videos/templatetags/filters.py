from datetime import datetime

from django import template

register = template.Library()


@register.filter
def custom_timesince(dt, default="now"):
    now = datetime.now()
    naive = dt.replace(tzinfo=None)
    diff = now - naive
    periods = (
        (diff.days / 365, "سال", "سال"),
        (diff.days / 30, "ماه", "ماه"),
        (diff.days / 7, "هفته", "هفته"),
        (diff.days, "روز", "روز"),
        (diff.seconds / 3600, "ساعت", "ساعت"),
        (diff.seconds / 60, "دقیقه", "دقیقه"),
        (diff.seconds, "ثانیه", "ثانیه"),
    )
    for period, singular, plural in periods:
        if period >= 1:
            return "%d %s پیش" % (period, singular if period == 1 else plural)
    return default
