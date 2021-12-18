from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.course_helpers import get_courses
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response
from attendance_manager.models import Notification

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserNotificationView(View):
    def get(self, request):
        student = request.student 
        course_ids = get_courses(student).values_list('course_id',flat=True)
        notifications = Notification.objects.filter(reciever_type=Notification.RecieverType.Department, reciever_id=student.department_id.department_id)
        notifications = notifications.union(Notification.objects.filter(reciever_type=Notification.RecieverType.Section, reciever_id=student.section_id.section_id))
        notifications = notifications.union(Notification.objects.filter(reciever_type=Notification.RecieverType.Course, reciever_id__in=course_ids))
        notifications = notifications.order_by('-date_of_sending')
        return successful_response(notifications)

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserNotificationDepartmentView(View):
    def get(self, request):
        student = request.student 
        notifications = Notification.objects.filter(reciever_type=Notification.RecieverType.Department, reciever_id=student.department_id.department_id)
        notifications = notifications.order_by('-date_of_sending')
        return successful_response(notifications)

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserNotificationSectionView(View):
    def get(self, request):
        student = request.student 
        notifications = Notification.objects.filter(reciever_type=Notification.RecieverType.Section, reciever_id=student.section_id.section_id)
        notifications = notifications.order_by('-date_of_sending')
        return successful_response(notifications)

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class UserNotificationCourseView(View):
    def get(self, request, course_id):
        student = request.student
        try:
            get_courses(student).get(course_id=course_id)
        except:
            return invalid_params_response('User does not have access to view the notifications')
        notifications = Notification.objects.filter(reciever_type=Notification.RecieverType.Course, reciever_id__in=course_id)
        notifications = notifications.order_by('-date_of_sending')
        return successful_response(notifications)