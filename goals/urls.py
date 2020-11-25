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
    path("api/v1/goals/new", goals.api_views.GoalCreate.as_view()),
    path("api/v1/goals/<int:id>/", goals.api_views.GoalRetrieveUpdateDestroy.as_view()),
]