import math
import random
import smtplib

def generateOTP() :
 
    # Declare a string variable 
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
    return OTP

def sendEmail(message, rollnumber):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("varunlingam.v@gmail.com", "140801071126@vssvVARUN")
    s.sendmail("sender_email_id", rollnumber + '@nitt.edu' , message)
    s.quit()