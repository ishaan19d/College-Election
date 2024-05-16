from django.urls import path
from .views import EmailSubmissionView, OTPVerificationView, AccountCreationView, StudentLoginView, PhDLoginView, LogoutView

urlpatterns = [
    path('submit_email/', EmailSubmissionView.as_view(), name='email_submission'),
    path('verify_otp/', OTPVerificationView.as_view(), name='otp_verification'),
    path('create_account/', AccountCreationView.as_view(), name='account_creation'),
    path('student-login/', StudentLoginView.as_view(), name='account_login'),
    path('phd-login/', PhDLoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
]