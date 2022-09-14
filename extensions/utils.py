import os
import math
import random


def username_from_email(email):
    return email.split("@")[0]


def get_extension_file(filename):
    return os.path.splitext(filename)[-1]


def generate_otp(length=6):
    digits = "0123456789"
    OTP = ""
    for i in range(length):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def numeric_month_to_name(month: int):
    jalali_month = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }
    return jalali_month[month]
