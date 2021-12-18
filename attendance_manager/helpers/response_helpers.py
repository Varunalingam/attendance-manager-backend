
from attendance_manager.models import Attendance, TimeTable


def successful_response(data):
    response = {
        'status_code':200,
        'data': data,
    }
    return response

def invalid_params_response(message = 'Bad Request'):
    '''
    defines the response sent out if the params are not valid
    '''

    response = {
        'status_code': 400,
        'data': message
    }

    return response


def unauthorized_response(message = 'Unauthorized. User credentials incorrect.'):
    '''
    defines the response sent out if the request is unauthorized
    '''

    response = {
        'status_code': 401,
        'data': message,
    }

    return response

def attendance_response(student, course):
    attendance = Attendance.objects.filter(student_id=student, timetable_id__course_id=course).exclude(timetable_id__status=TimeTable.Status.Suspended).order_by('-timetable_id__starttime')
    return successful_response(attendance)
