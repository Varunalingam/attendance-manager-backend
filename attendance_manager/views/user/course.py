import json
from django.views.generic import View

from attendance_manager.models import ClassRepresentative, CourseStudents, Courses

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.course_helpers import get_all_elective, get_courses
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response

from django.core.serializers.json import DjangoJSONEncoder
@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserCourseView(View):
    def get(self, request):
        student = request.student
        courses = get_courses(student)
        courses_list = courses.values('course_id', 'course_name', 'course_code', 'department_id__department_name', 'section_id', 'course_type', 'no_of_classes', 'minimum_attendance_percentage','credits')
        data = json.loads(json.dumps(list(courses_list), cls=DjangoJSONEncoder))
        for course in data:
            c = Courses.objects.get(course_id = course['course_id'])
            course['is_cr'] = False
            if ClassRepresentative.objects.filter(rep_of_id=course['course_id'], rep_of_type = ClassRepresentative.RepType.Course, student_id=student).count() == 1:
                course['is_cr'] = True
            elif c.section_id != None and ClassRepresentative.objects.filter(rep_of_id=c.section_id.section_id, rep_of_type = ClassRepresentative.RepType.Section, student_id=student).count() == 1:
                course['is_cr'] = True

        return successful_response(data)

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
