from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, UserProgress, WorkoutPlan
from django.core.exceptions import ValidationError
import re

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
        email = cleaned_data.get("email")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")

        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Введите правильный адрес электронной почты.")

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError(
                "Пароль должен содержать как минимум 8 символов."
            )
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "Пароль должен содержать как минимум одну заглавную букву."
            )
        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "Пароль должен содержать как минимум одну цифру."
            )
        return password


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["age", "weight", "height", "has_equipment"]

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and age <= 0:
            raise ValidationError("Возраст должен быть положительным числом.")
        return age

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is not None and weight <= 0:
            raise ValidationError("Вес должен быть положительным числом.")
        return weight

    def clean_height(self):
        height = self.cleaned_data.get("height")
        if height is not None and height <= 0:
            raise ValidationError("Рост должен быть положительным числом.")
        return height


class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ["weight", "workout_completed", "notes"]

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is not None and weight <= 0:
            raise ValidationError("Вес должен быть положительным числом.")
        return weight


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["name", "description", "equipment_required", "intensity_level"]

    def clean_intensity_level(self):
        intensity_level = self.cleaned_data.get("intensity_level")
        if intensity_level not in ["низкий", "средний", "высокий"]:
            raise ValidationError(
                "Интенсивность должна быть низкой, средней или высокой."
            )
        return intensity_level
