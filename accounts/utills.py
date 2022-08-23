import math
import random


def generate_otp(length=6):
    digits = "0123456789"
    OTP = ""
    for i in range(length):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def send_otp(phone):
    otp = generate_otp()
