import time
import math
import random


def generate_otp():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be changed
   # by changing value in range
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP
