from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, UserProgress, WorkoutPlan, CustomUser
from django.contrib import messages


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit)
        messages.success(self.request, "Регистрация прошла успешно!")
        return user


class UserProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ("male", "Мужской"),
        ("female", "Женский"),
        ("other", "Другой"),
    ]

    FITNESS_LEVEL_CHOICES = [
        ("beginner", "Начинающий"),
        ("below_average", "Ниже среднего"),
        ("average", "Средний"),
        ("above_average", "Выше среднего"),
        ("advanced", "Продвинутый"),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Пол",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True
    )
    fitness_level = forms.ChoiceField(
        choices=FITNESS_LEVEL_CHOICES,
        label="Уровень физической подготовки",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = UserProfile
        fields = [
            "age",
            "weight",
            "height",
            "has_equipment",
            "gender",
            "fitness_level",
            "chest_circumference",
            "arm_circumference",
            "leg_circumference",
            "waist_circumference"
        ]

    chest_circumference = forms.FloatField(
        required=False,
        label="Объём груди",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    arm_circumference = forms.FloatField(
        required=False,
        label="Объём рук",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    leg_circumference = forms.FloatField(
        required=False,
        label="Объём ног",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    waist_circumference = forms.FloatField(
        required=False,
        label="Объём талии",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )


class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ["weight", "workout_completed", "notes"]


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = [
            "name",
            "description",
            "equipment_required",
            "intensity_level",
            "scheduled_date",
        ]
