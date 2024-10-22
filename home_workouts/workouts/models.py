from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserProfile(models.Model):
    FITNESS_LEVEL_CHOICES = [
        ("beginner", "Начальный"),
        ("below_average", "Ниже среднего"),
        ("average", "Средний"),
        ("above_average", "Выше среднего"),
        ("advanced", "Продвинутый"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=18)
    weight = models.FloatField(default=70.0)
    height = models.FloatField(default=170.0)

    # Новые поля для объёмов тела
    chest_circumference = models.FloatField(
        null=True, blank=True, verbose_name="Объём груди"
    )
    arm_circumference = models.FloatField(
        null=True, blank=True, verbose_name="Объём рук"
    )
    leg_circumference = models.FloatField(
        null=True, blank=True, verbose_name="Объём ног"
    )
    waist_circumference = models.FloatField(
        null=True, blank=True, verbose_name="Объём талии"
    )

    has_equipment = models.BooleanField(default=False)
    fitness_level = models.CharField(
        max_length=20,
        choices=FITNESS_LEVEL_CHOICES,
        default="beginner",
    )

    def clean(self):
        if self.age < 0:
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    equipment_required = models.BooleanField(default=False)
    intensity_level = models.CharField(max_length=10, choices=INTENSITY_CHOICES)
    scheduled_date = models.DateField(null=True, blank=True)

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
        return f"{self.user.username} - {self.date} (Вес: {self.weight})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Пользователь должен иметь адрес электронной почты")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_description = models.CharField(max_length=255)
    date_set = models.DateField(auto_now_add=True)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.goal_description}"
