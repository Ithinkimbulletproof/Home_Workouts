
from django.contrib import admin
from .models import UserProfile, WorkoutPlan, UserProgress

admin.site.register(UserProfile)
admin.site.register(WorkoutPlan)
admin.site.register(UserProgress)
