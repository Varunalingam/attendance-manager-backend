from rest_framework.authtoken.models import Token
from attendance_manager.models import Student
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response, unauthorized_response

def RequiresTokenDecorator(view):
    """
    Checks whether the current session is up-to-date with the
    sessions in the backend
    """

    def wrapper(*args, **kwargs):

        try:
            request = args[0]
            token = request.headers['Authorization']

            user = Token.objects.get(key=token).user

            student = Student.objects.get(roll_no = user)

            args[0].user = student
            args[0].student = student

        except Exception as e:
            return unauthorized_response()
        
        return view(*args, **kwargs)

    return wrapper