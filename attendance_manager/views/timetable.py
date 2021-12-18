from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response
from attendance_manager.helpers.timetable_helpers import check_cr_permission_course
from attendance_manager.models import Courses, TimeTable

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class TimeTableCreateView(View):
    def post(self, request):
        student = request.student
        course_id = request.POST.get('course_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if start_time > end_time:
            return invalid_params_response('Start Time cannot be after End Time')

        try:
            course = Courses.objects.get(course_id=course_id)
            if not check_cr_permission_course(student, course):
                raise Exception('No CR Permission')
        except:
            return invalid_params_response('User does not have access to create timetable for the course')

        timetables = TimeTable.objects.filter(course_id=course).order_by('-starttime')
        if not (timetables.first().endtime < start_time):
            return invalid_params_response('there exists a class which has not yet completed for the given course')
        TimeTable.objects.create(course_id = course, starttime=start_time, endtime=end_time, status= TimeTable.Status.Active)
        return successful_response('Time table slot added successfully!')

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class TimeTableModifyView(View):
    def post(self, request):
        student = request.student
        timetable_id = request.POST.get('timetable_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        suspended = request.POST.get('suspended')
        if start_time > end_time:
            return invalid_params_response('Start Time cannot be after End Time')
        
        try:
            timetable = TimeTable.objects.get(timetable_id=timetable_id)
            if not check_cr_permission_course(student, timetable.course_id):
                raise Exception('No CR Permission')
        except:
            return invalid_params_response('User does not have access to create timetable for the course')
        
        timetables = TimeTable.objects.filter(course_id=timetable.course_id).exclude(timetable_id=timetable_id.timetable_id).order_by('-starttime')
        if not (timetables.first.endtime < start_time):
            return invalid_params_response('there exists a class which has not yet completed for the given course')
        
        timetable.starttime = start_time
        timetable.endtime = end_time
        timetable.status = TimeTable.Status.Modified
        if suspended:
            timetable.status = TimeTable.Status.Suspended
        timetable.save()
        return successful_response('Time table slot modified successfully!')

