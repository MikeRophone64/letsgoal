from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Profile(models.Model):
    user                =   models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture     =   models.URLField()
    date_of_birth       =   models.DateField(blank=True)

class Goal(models.Model):
    pass

class NewClass(models.Model):
    pass