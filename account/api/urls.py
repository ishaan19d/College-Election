from django.urls import path
from .views import EmailSubmissionView, OTPVerificationView, AccountCreationView, LoginView, LogoutView

urlpatterns = [
    path('submit_email/', EmailSubmissionView.as_view(), name='email_submission'),
    path('verify_otp/', OTPVerificationView.as_view(), name='otp_verification'),
    path('create_account/', AccountCreationView.as_view(), name='account_creation'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
]