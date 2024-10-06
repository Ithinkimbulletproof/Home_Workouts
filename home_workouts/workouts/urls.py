from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("workouts/", views.workout_list, name="workout_list"),
    path("workouts/<int:id>/", views.workout_detail, name="workout_detail"),
    path("progress/", views.progress, name="progress"),
    path("workout-plan/", views.workout_plan, name="workout_plan"),
]
