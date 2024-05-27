import random
import re
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Student, GradStudent, PhDStudent, PollingOfficer
from .serializers import GradStudentSerializer, PhDSerializer, StudentPhotoSerializer
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenViewBase
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

class EmailSubmissionView(APIView):
    def post(self, request):
        email = request.data.get('email')
        pattern = r'^[a-zA-Z]+\.[a-zA-Z]+([0-9]{2}[a-zA-Z])?@iiitg\.ac\.in$'
        if not re.match(pattern, email):
            return Response({'error': 'Please provide a valid college email address.'}, status=status.HTTP_400_BAD_REQUEST)

        if re.search(r'[0-9]{2}', email):
            if GradStudent.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if PhDStudent.objects.filter(email=email).exists():
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
                serializer = GradStudentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif course_type == 'm':
                data['course'] = 'M.Tech'
                data['graduating_year'] = year + 2002
                serializer = GradStudentSerializer(data=data)
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

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid email.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, student.password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if isinstance(student.get_real_instance(), GradStudent):
            student_type = 'Grad'
        elif isinstance(student.get_real_instance(), PhDStudent):
            student_type = 'PhD'
        else:
            print("The student is neither a GradStudent nor a PhDStudent.")
        token_payload = {
            'email': student.email,
            'student_type': student_type
        }

        token = RefreshToken()
        token.payload.update(token_payload)

        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_200_OK)
    
class PollingOfficerLoginView(TokenViewBase):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            polling_officer = PollingOfficer.objects.get(email=email)
        except PollingOfficer.DoesNotExist:
            return Response({'error': 'Invalid email.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not check_password(password,polling_officer.password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = RefreshToken()
        token_payload = {
            'email': polling_officer.email,
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
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(APIView):
    def post(self,request):
        email = request.data.get('email')
        acc_type = request.data.get('acc_type')
        if not email or not acc_type:
            return Response({'error': 'Email and account type is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if(acc_type == 'student'):
                Student.objects.get(email=email)
            elif(acc_type == 'polling_officer'):
                PollingOfficer.objects.get(email=email)
        except:
            return Response({'error': 'Account not found.'}, status=status.HTTP_404_NOT_FOUND)
        otp = random.randint(100000, 999999)
        send_mail(
            'OTP to change password',
            f'Your OTP is: {otp}',
            'ishaandas1910@gmail.com',
            [email],
            fail_silently=False,
        )
        token_payload = {
            'email': email,
            'otp': str(otp),
            'acc_type': acc_type,
        }
        token = RefreshToken()
        token_payload = {
            'email':email,
            'otp':str(otp),
            'acc_type':acc_type,
        }
        token.payload.update(token_payload)
        token_str = str(token.access_token)

        return Response({'token': token_str}, status=status.HTTP_200_OK)
    
class ResetPassword(APIView):
    def patch(self, request):
        token_str = request.data.get('token')
        otp = request.data.get('otp')

        try:
            token = AccessToken(token_str)
            payload = token.payload
            stored_otp = payload.get('otp')
            if str(stored_otp) == otp:
                if(payload.get('acc_type') == 'student'):
                    student = Student.objects.get(email=payload.get('email'))
                    student.password = make_password(request.data.get('password'))
                    student.save()
                elif(payload.get('acc_type') == 'polling_officer'):
                    polling_officer = PollingOfficer.objects.get(email=payload.get('email'))
                    polling_officer.password = make_password(request.data.get('password'))
                    polling_officer.save()
                return Response({'message': 'Password changes successfully.'}, status=status.HTTP_200_OK)
        except Exception:
                pass
        return Response({'error': 'Invalid OTP or token.'}, status=status.HTTP_400_BAD_REQUEST)
    
class ChangeProfilePhoto(APIView):
    def patch(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decoded_token.payload.get('email')
        if not email:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = Student.objects.filter(email=email).first()
            serializer = StudentPhotoSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Photo updated successfully.'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)