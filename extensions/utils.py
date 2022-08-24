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
