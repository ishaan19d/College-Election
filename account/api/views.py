import random
import re
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Student
from .serializers import StudentSerializer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from django.contrib.auth import get_user_model

class EmailSubmissionView(APIView):
    def post(self, request):
        email = request.data.get('email')
        pattern = r'^[a-zA-Z]+\.[a-zA-Z]+([0-9]{2}[bm])@iiitg\.ac\.in$'
        if not re.match(pattern, email):
            return Response({'error': 'Please provide a valid college email address.'}, status=status.HTTP_400_BAD_REQUEST)

        if Student.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        send_mail(
            'OTP for Student Registration',
            f'Your OTP for student registration is: {otp}',
            'ishaandas1910@gmail.com',
            [email],
            fail_silently=False,
        )

        token_payload = {
            'email': email,
            'otp': str(otp),
        }
        token = RefreshToken()
        token_payload = {
            'email':email,
            'otp':str(otp),
        }
        token.payload.update(token_payload)
        token_str = str(token.access_token)

        return Response({'token': token_str}, status=status.HTTP_200_OK)

class OTPVerificationView(APIView):
    def post(self, request):
        token_str = request.data.get('token')
        otp = request.data.get('otp')

        try:
            token = AccessToken(token_str)
            payload = token.payload
            stored_otp = payload.get('otp')
            if str(stored_otp) == otp:
                new_token_payload = {
                    'email': payload.get('email'),
                    'otp_verified': True,
                }
                new_token = RefreshToken()
                new_token.payload.update(new_token_payload)
                new_token_str = str(new_token.access_token)
                return Response({'message': 'OTP verified successfully.', 'token':new_token_str}, status=status.HTTP_200_OK)
        except Exception:
            pass

        return Response({'error': 'Invalid OTP or token.'}, status=status.HTTP_400_BAD_REQUEST)

class AccountCreationView(APIView):
    def post(self, request):
        token_str = request.data.get('token')
        try:
            token = AccessToken(token_str)
            payload = token.payload
            email = payload.get('email')
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        if email is None:
            return Response({'error': 'Email not found in token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not payload.get('otp_verified'):
            return Response({'error': 'OTP not verified.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email_parts = email.split('@')[0].split('.')
        year = int(email_parts[-1][-3:-1])
        course_type = email_parts[-1][-1].lower()

        data = request.data.copy()
        data['email'] = email
        if course_type == 'b':
            data['course'] = 'B.Tech'
            data['graduating_year'] = year + 2004
        elif course_type == 'm':
            data['course'] = 'M.Tech'
            data['graduating_year'] = year + 2002
        else:
            return Response({'error': 'Invalid course type in email.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        UserModel = get_user_model()
        user = UserModel.objects.filter(email=email).first()
        
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class LogoutView(TokenViewBase):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)