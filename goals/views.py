import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from .models import User, Profile, Goal, Like

from .error import catch


# Create your views here.
@login_required(login_url="goals:login")
def index(request):
    user = request.user
    goals = Goal.objects.all()
    return render(request, 'goals/index.html', context= {
        "goals": goals
    })


def register(request):
    if request.method == "POST":

        # get elements
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password_confirm = request.POST["confirm"]

        # check if passwords match
        if password != password_confirm:

            messages.info(request, "Passwords do not match...", extra_tags="danger")
            return render(request, 'goals/register.html')
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.info(request, "Username already taken...", extra_tags="danger")
            return HttpResponseRedirect('register')

        login(request, user)
        return HttpResponseRedirect('index')

    return render(request, 'goals/register.html')



def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            catch(user)
            login(request, user)
            return HttpResponseRedirect(reverse("goals:index"))
        else:
            messages.info(request, "Try again...", extra_tags="danger")
            return HttpResponseRedirect(reverse("goals:login"))
    
    return render(request, "goals/login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out!", extra_tags="success")
    return HttpResponseRedirect(reverse("goals:index"))