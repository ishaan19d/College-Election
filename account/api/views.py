import random
import re
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Student,PhD
from .serializers import StudentSerializer, PhDSerializer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class EmailSubmissionView(APIView):
    def post(self, request):
        email = request.data.get('email')
        pattern = r'^[a-zA-Z]+\.[a-zA-Z]+([0-9]{2}[a-zA-Z])?@iiitg\.ac\.in$'
        if not re.match(pattern, email):
            return Response({'error': 'Please provide a valid college email address.'}, status=status.HTTP_400_BAD_REQUEST)

        if re.search(r'[0-9]{2}', email):
            if Student.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if PhD.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        send_mail(
            'OTP for Registration',
            f'Your OTP for registration is: {otp}',
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
        data = request.data.copy()
        data['email'] = email

        if re.search(r'[0-9]{2}', email):
            year = int(email_parts[-1][-3:-1])
            course_type = email_parts[-1][-1].lower()
            if course_type == 'b':
                data['course'] = 'B.Tech'
                data['graduating_year'] = year + 2004
                serializer = StudentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif course_type == 'm':
                data['course'] = 'M.Tech'
                data['graduating_year'] = year + 2002
                serializer = StudentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid course type in email.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PhDSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentLoginView(TokenViewBase):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        student = Student.objects.filter(email=email).first()

        if student is None or not student.check_password(password):
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = RefreshToken()
        token_payload = {
            'email': student.email,
        }
        token.payload.update(token_payload)
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
            }, status=status.HTTP_200_OK)

        
class PhDLoginView(TokenViewBase):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        phd = PhD.objects.filter(email=email).first()
        if phd is None or not phd.check_password(password):
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        token = RefreshToken()
        token_payload = {
            'email': phd.email,
        }
        token.payload.update(token_payload)
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
            }, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)