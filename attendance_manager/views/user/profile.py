from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.response_helpers import invalid_params_response, retry_with_response, successful_response

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        student = request.student
        data = {
            'roll_number': student.roll_no,
            'name': student.name,
            'department_name':student.department_id.department_name,
            'section':student.section_id.section_name,
            'batch':student.batch.year 
        }
        return successful_response(data)

    def post(self, request):
        student = request.student
        name = request.POST.get('name')
        if name == None:
            return invalid_params_response("Name cannot be null!")
        if not str(name).isalpha():
            return invalid_params_response("Name need to contain only alphabets")
        
        student.name = str(name).title()
        student.save()
        
        return successful_response("Profile Updated Sucessfully!")
