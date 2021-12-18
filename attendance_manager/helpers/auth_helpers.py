import math
import random
import smtplib

from attendance_manager.models import Student
from django.utils import timezone
from datetime import timedelta

def generateOTP() :
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
    return OTP

def sendEmail(message, rollnumber):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("akilanforpresident@gmail.com", "Aapr15331")
    s.sendmail("akilanforpresident@gmail.com", rollnumber + '@nitt.edu' , message)
    s.quit()

def createOTP(roll_number):
    student = Student.objects.get(roll_no=roll_number)
    student.otp = generateOTP()
    student.otp_timeout = timezone.now() + timedelta(minutes=5)
    student.save()
    sendEmail(student.otp, student.roll_no)