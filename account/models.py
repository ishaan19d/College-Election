from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

COURSE_CHOICES = [
    ('B.Tech', 'B.Tech'),
    ('M.Tech', 'M.Tech'),
]

DEPARTMENT_CHOICES = [
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
]

class Student(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=7, choices=COURSE_CHOICES)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    graduating_year = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'roll_number', 'course', 'department', 'graduating_year']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='student_set',
        related_query_name='student',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='student_set',
        related_query_name='student',
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"


DEPARTMENT_CHOICES_PHD = [
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('HSS', 'HSS'),
    ('S&M', 'S&M'),
]

class PhD(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    course = 'PhD'
    ongoing = models.BooleanField(default=True)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES_PHD)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'roll_number', 'course', 'department']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='phd_set',
        related_query_name='phd',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='phd_set',
        related_query_name='phd',
    )

    class Meta:
        verbose_name = 'PhD'
        verbose_name_plural = 'PhDs'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"