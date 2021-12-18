from django.views.generic import View

from attendance_manager.models import CourseStudents, Courses

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.course_helpers import get_all_elective, get_courses
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserCourseView(View):
    def get(self, request):
        student = request.student
        return successful_response(get_courses(student))

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserCourseJoinView(View):
    def get(self, request):
        student = request.student
        return successful_response(get_all_elective(student))
    def post(self, request):
        student = request.student
        course_id = request.POST.get('course_id')
        try:
            course = Courses.objects.get(course_id = course_id)
        except:
            return invalid_params_response("Course Does Not Exist!")
        if course.course_type == Courses.CourseType.Program_Core or course.course_type == Courses.CourseType.Labratory_Requirement or course.course_type == Courses.CourseType.Institute_Requirement:
            return invalid_params_response("You are not Allowed to Join the Course!")
        CourseStudents.objects.get_or_create(course_id=course, student_id = student)
        return successful_response("Joined the Course Successfully")

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserCourseLeaveView(View):
    def post(self, request):
        student = request.student
        course_id = request.POST.get('course_id')
        try:
            course = Courses.objects.get(course_id = course_id)
            if course.course_type == Courses.CourseType.Program_Core or course.course_type == Courses.CourseType.Labratory_Requirement or course.course_type == Courses.CourseType.Institute_Requirement:
                return invalid_params_response("You are not Allowed to Leave the Course!")
            
            course_registration = CourseStudents.objects.get(course_id=course, student_id = student)
        except:
            return invalid_params_response("Course Does Not Exist!")
        
        course_registration.delete()
        return successful_response("Left the Course Successfully")
