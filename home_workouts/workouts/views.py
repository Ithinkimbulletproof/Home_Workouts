from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import UserRegistrationForm, UserProfileForm, UserProgressForm, WorkoutPlanForm
from .models import WorkoutPlan, UserProgress, UserProfile

def home(request):
    return render(request, "workouts/home.html")

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect("profile")
        else:
            messages.error(request, "Ошибка регистрации. Проверьте данные и попробуйте снова.")
    else:
        form = UserRegistrationForm()
    return render(request, "workouts/register.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("home")

@login_required
def profile(request):
    user = request.user
    # Создаем профиль, если его нет
    if not hasattr(user, 'userprofile'):
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

@login_required
def create_workout(request):
    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Тренировка успешно создана!")
            return redirect("workout_list")
    else:
        form = WorkoutPlanForm()
    return render(request, "workouts/create_workout.html", {"form": form})

class UserProgressView(TemplateView):
    template_name = "workouts/progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress_data"] = UserProgress.objects.filter(
            user=self.request.user
        ).order_by("-date")
        return context
