from django.db import models

class PollingOfficer(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

COURSE_CHOICES = [
    ('B.Tech', 'B.Tech'),
    ('M.Tech', 'M.Tech'),
]

DEPARTMENT_CHOICES = [
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('HSS', 'HSS'),
    ('SNM', 'SNM'),
]

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    roll_number = models.CharField(max_length=8, unique=True)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)

    def get_real_instance(self):
        if hasattr(self, 'gradstudent'):
            return self.gradstudent
        elif hasattr(self, 'phdstudent'):
            return self.phdstudent
        return self

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.roll_number}"

class GradStudent(Student):
    course = models.CharField(max_length=7, choices=COURSE_CHOICES)
    graduating_year = models.PositiveIntegerField()

class PhDStudent(Student):
    course = models.CharField(max_length=3, default='PhD', editable=False)
    ongoing = models.BooleanField(default=True)
