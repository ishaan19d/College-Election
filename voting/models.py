from django.db import models
from account.models import Student

POSITION_CHOICES = [
    ('President', 'President'),
    ('Vice President', 'Vice President'),
    ('General Secretary - Cultural Board', 'General Secretary - Cultural Board'),
    ('General Secretary - Technical Board', 'General Secretary - Technical Board'),
    ('General Secretary - Sports Board', 'General Secretary - Sports Board'),
    ('General Secretary - Welfare Board', 'General Secretary - Welfare Board'),
]

class ContestingCandidate(models.Model):
    candidate = models.OneToOneField(Student, primary_key=True, on_delete=models.CASCADE, to_field='roll_number')
    position = models.CharField(max_length=36,choices=POSITION_CHOICES)
    description = models.TextField()
    manifesto = models.FileField(upload_to='manifestos/', null=True, blank=True)
    nominated_by = models.EmailField(default=None, null=True, blank=True)
    faculty_approval_by = models.EmailField(default=None, null=True, blank=True)
    nomination_approved = models.BooleanField(default=None, null=True, blank=True)
    vote_count = models.PositiveIntegerField(default=0)
    vote_count_signature = models.BinaryField(default=None,null=True, blank=True)

    def __str__(self):
        return f"{self.candidate.first_name} {self.candidate.last_name} - {self.position}"

class Vote(models.Model):
    voter = models.ForeignKey(Student, on_delete=models.CASCADE, to_field='roll_number')
    position = models.CharField(max_length=36, choices=POSITION_CHOICES)

    def __str__(self):
        return f"Voter: {self.voter.roll_number}, Position: {self.position}"