from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import (
    UserRegistrationForm,
    UserProfileForm,
    UserProgressForm,
    WorkoutPlanForm,
)
from .models import WorkoutPlan, UserProgress, UserProfile, UserGoal
from datetime import datetime
from django.db.models.functions import ExtractWeek


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        else:
            messages.error(
                request, "Ошибка регистрации. Проверьте данные и попробуйте снова."
            )
    else:
        form = UserRegistrationForm()

    return render(request, "workouts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    user = request.user
    if not hasattr(user, "userprofile"):
        UserProfile.objects.create(user=user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль обновлен!")
            return redirect("workout_plan")
        else:
            messages.error(request, "Ошибка при сохранении данных. Проверьте форму.")
    else:
        form = UserProfileForm(instance=user.userprofile)

    return render(request, "workouts/profile.html", {"form": form})


@login_required
def workout_plan(request):
    user_profile = request.user.userprofile
    workouts = WorkoutPlan.objects.filter(equipment_required=user_profile.has_equipment)
    return render(request, "workouts/workout_plan.html", {"workouts": workouts})


@login_required
def workout_list(request):
    workouts = WorkoutPlan.objects.all()
    return render(request, "workouts/workout_list.html", {"workouts": workouts})


@login_required
def workout_detail(request, id):
    workout = get_object_or_404(WorkoutPlan, id=id)
    return render(request, "workouts/workout_detail.html", {"workout": workout})


@login_required
def create_workout(request):
    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            user_profile = request.user.userprofile

            # Подбираем уровень физической подготовки и цели
            if user_profile.fitness_level >= workout.required_fitness_level:
                workout.user = request.user
                workout.save()
                messages.success(request, "Тренировка успешно создана!")
            else:
                messages.error(request, "Ваш уровень физической подготовки недостаточен для этой тренировки.")
                return render(request, "workouts/create_workout.html", {"form": form})

            return redirect("workout_list")
    else:
        form = WorkoutPlanForm()
    return render(request, "workouts/create_workout.html", {"form": form})


def home(request):
    if request.user.is_authenticated:
        return redirect("main")
    return render(request, "workouts/home.html")


@login_required
def main(request):
    user = request.user

    user_profile = request.user.userprofile
    workouts = WorkoutPlan.objects.filter(user=user).order_by("scheduled_date")[:5]

    planned_workouts_count = WorkoutPlan.objects.filter(
        user=user, scheduled_date__week=datetime.now().isocalendar()[1]
    ).count()

    user_goals = UserGoal.objects.filter(user=user)

    recommendations = [
        {"title": "Как правильно питаться во время тренировок", "url": "#"},
        {"title": "5 упражнений для новичков", "url": "#"},
    ]

    context = {
        "workouts": workouts,
        "user_goals": user_goals,
        "planned_workouts_count": planned_workouts_count,
        "recommendations": recommendations,
    }

    return render(request, "workouts/main.html", context)


class UserProgressView(TemplateView):
    template_name = "workouts/progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress_data"] = UserProgress.objects.filter(
            user=self.request.user
        ).order_by("-date")
        return context
