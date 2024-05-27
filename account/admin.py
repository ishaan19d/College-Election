from django.contrib import admin
from .models import Student, GradStudent, PhDStudent, PollingOfficer
# Register your models here.
admin.site.register(Student)
admin.site.register(GradStudent)
admin.site.register(PhDStudent)
admin.site.register(PollingOfficer)