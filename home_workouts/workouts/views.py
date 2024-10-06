from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, UserProgressForm
from .models import WorkoutPlan, UserProgress


def home(request):
    return render(request, "workouts/home.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "workouts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    return render(request, "workouts/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль обновлен!")
            return redirect("home")
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, "workouts/profile.html", {"form": form})


@login_required
def progress(request):
    if request.method == "POST":
        form = UserProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            messages.success(request, "Ваш прогресс сохранен!")
            return redirect("progress")
    else:
        form = UserProgressForm()

    progress_data = UserProgress.objects.filter(user=request.user).order_by("-date")
    return render(
        request,
        "workouts/progress.html",
        {"form": form, "progress_data": progress_data},
    )


@login_required
def workout_plan(request):
    user_profile = request.user.userprofile
    if user_profile.has_equipment:
        workouts = WorkoutPlan.objects.filter(equipment_required=True)
    else:
        workouts = WorkoutPlan.objects.filter(equipment_required=False)

    return render(request, "workouts/workout_plan.html", {"workouts": workouts})


@login_required
def workout_list(request):
    workouts = WorkoutPlan.objects.all()
    return render(request, "workouts/workout_list.html", {"workouts": workouts})


@login_required
def workout_detail(request, id):
    workout = WorkoutPlan.objects.get(id=id)
    return render(request, "workouts/workout_detail.html", {"workout": workout})
