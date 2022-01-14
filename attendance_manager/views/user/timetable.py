from datetime import datetime, time
import json
from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.course_helpers import get_courses
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response
from attendance_manager.models import Courses, TimeTable

from django.forms.models import model_to_dict

from django.utils import timezone

from django.core.serializers.json import DjangoJSONEncoder

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserTimetableView(View):
    def get(self, request):
        student = request.student
        today = request.POST.get('date')
        course_ids = get_courses(student).values_list('course_id', flat=True)
        timetable = TimeTable.objects.filter(course_id__in=course_ids,starttime__range=(datetime.combine(today, time.min), datetime.combine(today, time.max))).order_by('starttime')
        timetable = timetable.values('timetable_id', 'starttime', 'endtime', 'course_id', 'status')
        data = json.loads(json.dumps(list(timetable), cls=DjangoJSONEncoder))
        for timetable in data:
            c = Courses.objects.get(course_id = timetable['course_id'])
            timetable['course'] = json.loads(json.dumps(model_to_dict(c), cls=DjangoJSONEncoder))
        return successful_response(data)