from django.urls import path

from attendance_manager.views.auth import LoginRequestVerifyView, LoginRequestView
from attendance_manager.views.notification import NotificationCreateView, NotificationModifyView
from attendance_manager.views.timetable import TimeTableCreateView, TimeTableModifyView
from attendance_manager.views.user.attendance import UserAttendanceCourseView, UserAttendanceView
from attendance_manager.views.user.course import UserCourseJoinView, UserCourseView, UserCourseLeaveView
from attendance_manager.views.user.notification import UserNotificationCourseView, UserNotificationDepartmentView, UserNotificationSectionView, UserNotificationView
from attendance_manager.views.user.profile import UserProfileView
from attendance_manager.views.user.timetable import UserTimetableView

app_name = 'attendance_manager'

urlpatterns = [
    path('auth/login/request', LoginRequestView.as_view(), name='auth-login-request'),
    path('auth/login/verify', LoginRequestVerifyView.as_view(), name='auth-login-verify'),
    
    path('user/profile', UserProfileView.as_view(), name='user-profile'),
    
    path('user/courses', UserCourseView.as_view(), name='user-courses'),
    path('user/courses/join',UserCourseJoinView.as_view(), name='user-course-join'),
    path('user/courses/leave',UserCourseLeaveView.as_view(),name='user-course-leave'),
    
    path('user/timetable',UserTimetableView.as_view(), name='user-timetable'),
    
    path('user/notifications', UserNotificationView.as_view(), name='user-notification'),
    path('user/notifications/department', UserNotificationDepartmentView.as_view(), name='user-notification-department'),
    path('user/notifications/section', UserNotificationSectionView.as_view(), name='user-notification-section'),
    path('user/notifications/course/{course_id}', UserNotificationCourseView.as_view(), name='user-notification-course'),
    
    path('user/attendance',UserAttendanceView.as_view(),name='user-attendance'),
    path('user/attendance/{course_id}',UserAttendanceCourseView.as_view(),name='user-attendance-course'),

    path('timetable/create', TimeTableCreateView.as_view(),name='timetable-create'),
    path('timetable/edit', TimeTableModifyView.as_view(), name='timetable-modify'),

    path('notification/create', NotificationCreateView.as_view(), name='notification-create'),
    path('notification/edit', NotificationModifyView.as_view(), name='notification-edit')
]