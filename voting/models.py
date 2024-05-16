from django.db import models
from account.models import Student

POSITION_CHOICES = [
    ('President', 'President'),
    ('Vice President', 'Vice President'),
    ('General Secretary - Cultural Board', 'General Secretary - Cultural Board'),
    ('General Secretary - Technical Board', 'General Secretary - Technical Board'),
    ('General Secretary - Sports Board', 'General Secretary - Sports Board'),
]

class ContestingCandidate(models.Model):
    candidate = models.OneToOneField(Student, primary_key=True, on_delete=models.CASCADE, to_field='roll_number')
    position = models.CharField(max_length=36,choices=POSITION_CHOICES)
    por_description = models.TextField()
    manifesto = models.FileField(upload_to='manifestos/', null=True, blank=True)
    is_approved = models.BooleanField(default=None)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.candidate.first_name} {self.candidate.last_name} - {self.position}"

class Vote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, to_field='roll_number')
    candidate = models.ForeignKey(ContestingCandidate, on_delete=models.CASCADE, to_field='candidate')