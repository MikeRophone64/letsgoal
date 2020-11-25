from django.urls import path
from . import views
import goals.api_views

app_name = "goals"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API views
    path("api/v1/goals/", goals.api_views.GoalList.as_view()),
]