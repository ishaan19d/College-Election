from rest_framework import permissions
from account.models import Student
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
class IsStudentAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        access_token = request.data.get('access_token')
        if not access_token:
            return False

        try:
            decoded_token = AccessToken(access_token)
        except InvalidToken:
            return False

        email = decoded_token.payload.get('email')
        if not email:
            return False

        student = Student.objects.filter(email=email).first()
        return bool(student)