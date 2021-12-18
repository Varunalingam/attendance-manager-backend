from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.course_helpers import get_courses
from attendance_manager.helpers.response_helpers import attendance_response, invalid_params_response
from attendance_manager.models import Attendance, Courses, TimeTable

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserAttendanceView(View):
    def post(self, request):
        student=request.student
        timetable_id = request.POST.get('timetable_id')
        attendance_status = request.POST.get('attendance')
        course_ids = get_courses(student).values_list('course_id')
        try:
            timetable = TimeTable.objects.get(timetable_id=timetable_id, course_id__course_id__in=course_ids)
            attendance = Attendance.objects.get(student_id=student, timetable_id=timetable)
        except:
            return invalid_params_response('Timetable does not exist!')
        attendance.present_status = attendance_status
        attendance.save()
        return attendance_response(student, timetable.course_id)

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserAttendanceCourseView(View):
    def get(self, request, course_id):
        student=request.student
        course_ids = get_courses(student).values_list('course_id')
        if not course_id in course_ids:
            return invalid_params_response('Course does not exist!')
        course = Courses.objects.get(course_id=course_id)
        return attendance_response(student, course)