from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.login, name="login"),
    path("", views.register, name="register"),
]