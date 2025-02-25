from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('customers', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('customers/<int:pk>', CustomerRetrieveUpdateAPIView.as_view(), name='customer-detail'),

    path('managers', ManagerListCreateAPIView.as_view(), name='manager-list-create'),
    path('managers/<int:pk>', ManagerRetrieveUpdateDestroyAPIView.as_view(), name='manager-detail'),

    path('employees', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>', EmployeeRetrieveUpdateDestroyAPIView.as_view(), name='employee-detail'),

    path('forgot-password', ForgotPasswordAPIView.as_view(), name='forgot-password'),

    path('verify-otp/register', RegisterVerifyOTPAPIView.as_view(), name='verify-otp-register'),
    path('verify-otp/forgot-password', ForgotPasswordVerifyOTPAPIView.as_view(), name='verify-otp-forgot-password'),
    
    path('resend-otp/register', ResendRegisterOTPAPIView.as_view(), name='resend-otp-register'),
    path('resend-otp/forgot-password', ResendForgotPasswordOTPAPIView.as_view(), name='resend-otp-forgot-password'),

    path('reset-password', ResetPasswordAPIView.as_view(), name='reset-password'),

    path('change-password', ChangePasswordAPIView.as_view(), name='change-password'),

    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('log-out', LogoutAPIView.as_view(), name='log-out'),

    path("auth/google/login/", GoogleLoginAPIView.as_view(), name="google-login"),
    path("auth/facebook/login/", FacebookLoginAPIView.as_view(), name="facebook-login"),
    path("auth/linkedin/login/", LinkedInLoginAPIView.as_view(), name="linkedin-login"),
    path("auth/github/login/", GitHubLoginAPIView.as_view(), name="github-login"),
]
