from datetime import datetime, time
from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.course_helpers import get_courses
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response
from attendance_manager.models import TimeTable

from django.utils import timezone

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserTimetableView(View):
    def get(self, request):
        student = request.student
        today = timezone.now().date()
        course_ids = get_courses(student).values_list('course_id', flat=True)
        timetable = TimeTable.objects.filter(course_id__in=course_ids,starttime__range=(datetime.combine(today, time.min), datetime.combine(today, time.max))).order_by('starttime')
        timetable = timetable.values('timetable_id', 'starttime', 'endtime', 'course_id', 'status', 'course_id__course_name', 'course_id__course_code')
        return successful_response(timetable)