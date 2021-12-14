from time import time
from django.views.generic import View
from attendance_manager.helpers.auth_helpers import generateOTP, sendEmail
from attendance_manager.models import Student

from datetime import datetime, timedelta

class LoginRequestView(View):
    def post(self, request):
        roll_number = request.POST.get('roll_number')

        if not Student.objects.filter(roll_no = roll_number).exists():
            student = Student(roll_no=roll_number)
            student.save()
        
        student = Student.objects.get(roll_no=roll_number)
        student.otp = generateOTP()
        student.otp_timeout = datetime.now() + timedelta(minutes=5)
        student.save()
        sendEmail(student.otp, student.rollnumber)
        