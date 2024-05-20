from django.contrib import admin
from .models import Student, PhD, PollingOfficer
# Register your models here.
admin.site.register(Student)
admin.site.register(PhD)
admin.site.register(PollingOfficer)