
import json
from django.core.serializers.json import DjangoJSONEncoder
from attendance_manager.models import Attendance, Courses, Department, Section, TimeTable


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

def retry_with_response(message = 'Retry After Performing the necessary steps'):
    '''
    defines the response sent out if the request is early
    '''

    response = {
        'status_code': 449,
        'data': message,
    }

    return response

def attendance_response(student, course):
    attendance = Attendance.objects.filter(student_id=student, timetable_id__course_id=course).exclude(timetable_id__status=TimeTable.Status.Suspended).order_by('-timetable_id__starttime')
    return successful_response(attendance)

def notification_response(notifications):
    data = json.loads(json.dumps(list(notifications), cls=DjangoJSONEncoder))
    for notification in data:
        receiver_id = notification['receiver_id']
        if notification['reciever_type'] == 'D':
            notification['recieved_from'] = Department.objects.get(department_id=receiver_id).department_name
        elif notification['reciever_type'] == 'S':
            section = Section.objects.get(section_id=receiver_id)
            notification['recieved_from'] = section.section_name + ' - ' + section.department.department_name + ' - ' + str(section.batch.year)
        else:
            course = Courses.objects.get(course_id=receiver_id)
            notification['recieved_from'] = course.course_code + ' - ' + course.cOurse_name
    return successful_response(data)

