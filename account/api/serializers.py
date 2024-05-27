from rest_framework import serializers
from account.models import GradStudent, PhDStudent, PollingOfficer, Student
from django.contrib.auth.hashers import make_password

class GradStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = GradStudent
        fields = ['email', 'password', 'first_name', 'middle_name', 'last_name', 'roll_number', 'course', 'department', 'graduating_year', 'photo']

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        student_data = {
            'first_name': validated_data.get('first_name'),
            'middle_name': validated_data.get('middle_name'),
            'last_name': validated_data.get('last_name'),
            'email': validated_data.get('email'),
            'roll_number': validated_data.get('roll_number'),
            'department': validated_data.get('department'),
            'photo': validated_data.get('photo'),
            'password': hashed_password,
            'course': validated_data.get('course'),
            'graduating_year': validated_data.get('graduating_year'),
        }

        grad_student = GradStudent.objects.create(**student_data)
        return grad_student

class PhDSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = PhDStudent
        fields = ['email','password', 'first_name', 'middle_name', 'last_name', 'roll_number', 'department', 'ongoing', 'photo']

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        student_data = {
            'first_name': validated_data.get('first_name'),
            'middle_name': validated_data.get('middle_name'),
            'last_name': validated_data.get('last_name'),
            'email': validated_data.get('email'),
            'roll_number': validated_data.get('roll_number'),
            'department': validated_data.get('department'),
            'photo': validated_data.get('photo'),
            'password': hashed_password,
            'ongoing': validated_data.get('ongoing'),
        }

        phd_student = PhDStudent.objects.create(**student_data)
        return phd_student
    
class PollingOfficerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = PollingOfficer
        fields = ['email','password', 'first_name', 'middle_name', 'last_name', 'photo']

class StudentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['photo']