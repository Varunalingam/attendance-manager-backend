from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response


@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserProfileView(View):
    def post(self, request):
        name = request.POST.get('name')
        if name == None:
            return invalid_params_response("Name cannot be null!")
        if not str(name).isalpha():
            return invalid_params_response("Name need to contain only alphabets")
        
        request.student.name = str(name).title()
        request.student.save()
        
        return successful_response("Profile Updated Sucessfully!")
