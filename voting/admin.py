from django.contrib import admin
from .models import ContestingCandidate, Vote
# Register your models here.
admin.site.register(ContestingCandidate)
admin.site.register(Vote)