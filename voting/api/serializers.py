from rest_framework import serializers
from voting.models import ContestingCandidate
from account.models import Student, GradStudent, PhDStudent

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'middle_name' ,'last_name', 'roll_number' ,'photo')

class ContestingCandidateListSerializer(serializers.ModelSerializer):
    candidate = StudentListSerializer()
    class Meta:
        model = ContestingCandidate
        fields = ('candidate','position','is_approved')

class PhDStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhDStudent
        fields = ('first_name', 'middle_name' ,'last_name', 'roll_number', 'email', 'course', 'department', 'ongoing','photo')
    def to_representation(self, instance):
        real_instance = instance.get_real_instance()
        return super().to_representation(real_instance)

class GradStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradStudent
        fields = ('first_name', 'middle_name' ,'last_name', 'roll_number', 'email', 'course', 'department', 'graduating_year','photo')
    def to_representation(self, instance):
        real_instance = instance.get_real_instance()
        return super().to_representation(real_instance)

class ContestingCandidateSerializer(serializers.ModelSerializer):
    candidate = serializers.SerializerMethodField()

    class Meta:
        model = ContestingCandidate
        exclude = ['vote_count']

    def get_candidate(self, obj):
        real_instance = obj.candidate.get_real_instance()
        if isinstance(real_instance, GradStudent):
            serializer = GradStudentSerializer(real_instance)
        elif isinstance(real_instance, PhDStudent):
            serializer = PhDStudentSerializer(real_instance)
        else:
            raise ValueError("Unexpected candidate type")
        return serializer.data

class ResultSerializer(serializers.ModelSerializer):
    candidate = serializers.SerializerMethodField()

    class Meta:
        model = ContestingCandidate
        fields = ['candidate', 'vote_count']

    def get_candidate(self,obj):
        serializer = StudentListSerializer(obj.candidate)
        return serializer.data
