from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserProgressForm
from .models import WorkoutPlan, UserProgress


def home(request):
    return render(request, "workouts/home.html")


def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, "workouts/profile.html", {"form": form})


def progress(request):
    if request.method == "POST":
        form = UserProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            return redirect("progress")
    else:
        form = UserProgressForm()
        progress_data = UserProgress.objects.filter(user=request.user).order_by("-date")
    return render(
        request,
        "workouts/progress.html",
        {"form": form, "progress_data": progress_data},
    )


def workout_plan(request):
    user_profile = request.user.userprofile
    if user_profile.has_equipment:
        workouts = WorkoutPlan.objects.filter(equipment_required=True)
    else:
        workouts = WorkoutPlan.objects.filter(equipment_required=False)
    return render(request, "workouts/workout_plan.html", {"workouts": workouts})
