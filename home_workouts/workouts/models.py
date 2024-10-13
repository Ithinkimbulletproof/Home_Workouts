from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=18)
    weight = models.FloatField(default=70.0)
    height = models.FloatField(default=170.0)
    has_equipment = models.BooleanField(default=False)

    def clean(self):
        if self.age <= 0:
            raise ValidationError("Возраст должен быть положительным числом.")
        if self.weight <= 0:
            raise ValidationError("Вес должен быть положительным числом.")
        if self.height <= 0:
            raise ValidationError("Рост должен быть положительным числом.")

    def __str__(self):
        return self.user.username


class WorkoutPlan(models.Model):
    INTENSITY_CHOICES = [
        ("low", "Низкая"),
        ("medium", "Средняя"),
        ("high", "Высокая"),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    equipment_required = models.BooleanField(default=False)
    intensity_level = models.CharField(max_length=6, choices=INTENSITY_CHOICES)

    def __str__(self):
        return self.name


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    weight = models.FloatField()
    workout_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if self.weight <= 0:
            raise ValidationError("Вес должен быть положительным числом.")

    def __str__(self):
        return f"{self.user.username} - {self.date}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = BaseUserManager()
