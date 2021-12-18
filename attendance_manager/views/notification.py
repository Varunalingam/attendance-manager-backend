from django.utils import timezone
from django.views.generic import View

from django.utils.decorators import method_decorator
from attendance_manager.decorators.requires_token import RequiresTokenDecorator
from attendance_manager.decorators.response import JsonResponseDecorator
from attendance_manager.helpers.response_helpers import invalid_params_response, successful_response
from attendance_manager.helpers.timetable_helpers import check_cr_permission_course, check_cr_permission_section
from attendance_manager.models import Courses, Notification, TimeTable

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class NotificationCreateView(View):
    def post(self, request):
        student = request.student
        reciever_type = request.POST.get('reciever_type')
        reciever_id = request.POST.get('reciever_id')
        title = request.POST.get('title')
        body = request.POST.get('body')
        file_link = request.POST.get('file_link')

        if title != None:
            return invalid_params_response('Title cannot be Empty')
        
        title = str(title)

        try:
            if reciever_type == Notification.RecieverType.Course.name:
                course = Courses.objects.get(course_id=reciever_id)
                reciever_type = Notification.RecieverType.Course
                if not check_cr_permission_course(student, course):
                    raise Exception('No CR Permission')
            elif reciever_type == Notification.RecieverType.Section.name:
                reciever_type = Notification.RecieverType.Section
                reciever_id = student.section_id
                if not check_cr_permission_section(student):
                    raise Exception('No CR Permission')
            elif reciever_type == Notification.RecieverType.Department.name:
                reciever_type = Notification.RecieverType.Department
                reciever_id = student.department_id
                if not check_cr_permission_section(student):
                    raise Exception('No CR Permission')
            else:
                raise Exception('No CR Permission')
        except:
            return invalid_params_response('User does not have access to send notifications')

        Notification.objects.create(title = title, message = body, reciever_type = reciever_type, reciever_id = reciever_id, date_of_sending = timezone.now(),file_link = file_link)
        return successful_response('Notification created successfully!')

@method_decorator(RequiresTokenDecorator, name='dispatch')
@method_decorator(JsonResponseDecorator, name='dispatch')
class NotificationModifyView(View):
    def post(self, request):
        student = request.student
        notification_id = request.POST.get('notification_id')
        title = request.POST.get('title')
        body = request.POST.get('body')
        file_link = request.POST.get('file_link')

        if title != None:
            return invalid_params_response('Title cannot be Empty')
        
        title = str(title)

        try:
            notification = Notification.objects.get(notification_id = notification_id)
            if notification.reciever_type == Notification.RecieverType.Course:
                course = Courses.objects.get(course_id=notification.reciever_id)
                if not check_cr_permission_course(student, course):
                    raise Exception('No CR Permission')
            elif notification.reciever_type == Notification.RecieverType.Section and notification.reciever_id == student.section_id.section_id:
                if not check_cr_permission_section(student):
                    raise Exception('No CR Permission')
            elif notification.reciever_type == Notification.RecieverType.Department and notification.reciever_id == student.department_id.department_id:
                if not check_cr_permission_section(student):
                    raise Exception('No CR Permission')
            else:
                raise Exception('No CR Permission')
        except:
            return invalid_params_response('User does not have access to send notifications')
        
        notification.title = title
        notification.message = body
        notification.file_link = file_link
        notification.date_of_sending = timezone.now()
        notification.save()
        return successful_response('Notification modified successfully!')

