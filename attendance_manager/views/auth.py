from django.views.generic import View
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.auth_helpers import createOTP
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response, unauthorized_response

from attendance_manager.models import Student
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from django.utils import timezone

@method_decorator(JsonResponseDecorator, name='dispatch')
class LoginRequestView(View):
    def post(self, request):
        roll_number = request.POST.get('roll_number')

        if roll_number == None:
            return invalid_params_response('Roll number is a required field!')

        if not str(roll_number).isnumeric() and not len(str(roll_number)) == 9:
            return invalid_params_response('Roll number is a 9 digit numerical string!')

        if not Student.objects.filter(roll_no = roll_number).exists():
            
            student = Student.objects.create_user(roll_no=roll_number)
            student.save()
            
        createOTP(roll_number)
        student = Student.objects.get(roll_no=roll_number)
        return successful_response('OTP Sent Successfully !' + student.otp)

@method_decorator(JsonResponseDecorator, name='dispatch')
class LoginRequestVerifyView(View):
    def post(self, request):
        roll_number = request.POST.get('roll_number')

        if roll_number == None:
            return invalid_params_response('Roll number is a required field!')

        if not str(roll_number).isnumeric() and not len(str(roll_number)) == 9: 
            return invalid_params_response('Roll number is a 9 digit numeric field!')

        if not Student.objects.filter(roll_no = roll_number).exists():
            return invalid_params_response('Please use the correct roll number to login!')
        
        student = Student.objects.get(roll_no = roll_number)

        otp = request.POST.get('otp')
        
        if otp == None:
            return invalid_params_response('OTP is a required field!')

        if not len(str(otp)) == 6:
            return invalid_params_response('OTP is a 6 digit AlphaNumerical string!')

        if otp == student.otp and timezone.now() < student.otp_timeout:
            user = authenticate(username = student.roll_no, password="")
            token = Token.objects.get_or_create(user=user)
            student.otp_timeout = timezone.now()
            student.save()

            data = {
                'token': token[0].key
            }
            return successful_response(data)
        elif not timezone.now() < student.otp_timeout:
            createOTP(roll_number)
            return unauthorized_response('OTP has Timed Out! Retry with the newly sent OTP')
        else:
            return invalid_params_response('Invalid OTP')
        
