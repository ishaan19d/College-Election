from rest_framework import serializers
from account.models import Student, PhD

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'password', 'first_name', 'middle_name', 'last_name', 'roll_number', 'course', 'department', 'graduating_year', 'photo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Student(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PhDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhD
        fields = ['email', 'password', 'first_name', 'middle_name', 'last_name', 'roll_number', 'department', 'ongoing', 'photo']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        phd = PhD(**validated_data)
        phd.set_password(password)
        phd.save()
        return phd