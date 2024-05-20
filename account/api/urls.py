from django.urls import path
from .views import EmailSubmissionView, OTPVerificationView, AccountCreationView, StudentLoginView, PollingOfficerLoginView, LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register-email/', EmailSubmissionView.as_view(), name='email_registration'),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp_verification'),
    path('create-account/', AccountCreationView.as_view(), name='account_creation'),

    path('student-login/', StudentLoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),

    path('polling-officer-login/', PollingOfficerLoginView.as_view(), name='polling_officer_login'),
]