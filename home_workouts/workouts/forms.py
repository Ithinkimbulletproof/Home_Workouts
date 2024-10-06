from django import forms
from .models import UserProfile, UserProgress


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "weight", "height", "has_equipment"]


class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ["weight", "workout_completed", "notes"]
