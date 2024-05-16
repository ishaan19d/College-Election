from rest_framework import serializers
from voting.models import ContestingCandidate
from account.models import Student

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'middle_name' ,'last_name', 'roll_number' ,'photo')

class ContestingCandidateListSerializer(serializers.ModelSerializer):
    candidate = StudentListSerializer()
    class Meta:
        model = ContestingCandidate
        fields = ('candidate','position','is_approved')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'middle_name' ,'last_name', 'roll_number', 'email', 'course', 'department', 'graduating_year','photo')

class ContestingCandidateSerializer(serializers.ModelSerializer):
    candidate = StudentSerializer()
    class Meta:
        model = ContestingCandidate
        exclude = ['vote_count']
