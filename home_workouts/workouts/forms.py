from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, UserProgress


User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")

        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")

        if User.objects.filter(email=cleaned_data.get("email")).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "weight", "height", "has_equipment"]


class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ["weight", "workout_completed", "notes"]
