from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserProgress


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "weight", "height", "has_equipment"]


class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ["weight", "workout_completed", "notes"]
