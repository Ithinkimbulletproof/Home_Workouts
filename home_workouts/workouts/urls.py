from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("signup/", views.register, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="workouts/login.html"),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/<int:id>/", views.workout_detail, name="workout_detail"),
    path("progress/", views.UserProgressView.as_view(), name="progress"),
    path("workout-plan/", views.workout_plan, name="workout_plan"),
]
