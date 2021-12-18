from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response
from attendance_manager.models import CourseStudents, Courses, Section

from django.utils import timezone

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        student = request.student
        course_period = Courses.CoursePeriod.Winter
        if timezone.now().month < 6:
            course_period = Courses.CoursePeriod.Summer  
        course_year = timezone.now().date()
        course_year.day = 1
        course_year.month = 6
        courses = list(CourseStudents.objects.filter(student_id=student, course_id__course_period=course_period, course_id__course_year=course_year))
        courses += list(Courses.objects.filter(section_id=student.section_id, course_period=course_period, course_year=course_year))
        courses = list(set(courses))
        return successful_response(courses)