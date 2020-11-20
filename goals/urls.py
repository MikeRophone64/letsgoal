from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
]