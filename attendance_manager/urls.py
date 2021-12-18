from django.urls import path

from attendance_manager.views.auth import LoginRequestVerifyView, LoginRequestView
from attendance_manager.views.user.profile import UserProfileView

app_name = 'attendance_manager'

urlpatterns = [
    path('auth/login/request', LoginRequestView.as_view(), name='auth-login-request'),
    path('auth/login/verify', LoginRequestVerifyView.as_view(), name='auth-login-verify'),
    path('user/profile', UserProfileView.as_view(), name='user-profile')
]