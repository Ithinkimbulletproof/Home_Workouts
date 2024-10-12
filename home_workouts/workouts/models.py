from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    has_equipment = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class WorkoutPlan(models.Model):
    INTENSITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    equipment_required = models.BooleanField(default=False)
    intensity_level = models.CharField(max_length=50, choices=INTENSITY_CHOICES)

    def __str__(self):
        return self.name


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    weight = models.FloatField()
    workout_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
