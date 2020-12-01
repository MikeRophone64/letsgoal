import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from .models import User, Profile, Goal, Like, GoalStatus
from .forms import GoalForm

from .error import catch


# Create your views here.
@login_required(login_url="goals:login")
def index(request):
    current_user = User.objects.get(username=request.user)
    goals = Goal.objects.all()
    return render(request, 'goals/index.html', context= {
        "current_user": current_user,
        "GoalForm": GoalForm,
        "goals": goals
    })

@login_required(login_url="goals:login")
def new_goal(request):
    current_user = User.objects.get(username=request.user)

    if request.method == "POST":
        form = GoalForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            term = form.cleaned_data['term']
            deadline = form.cleaned_data['deadline']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            purpose = form.cleaned_data['purpose']
            status = GoalStatus.objects.get(pk=1)
            
            add = Goal.objects.create(title=title, created_by=current_user, term=term, deadline=deadline, category=category, description=description, purpose=purpose, status=status)
            add.save()
            catch(add.id)
        return HttpResponseRedirect(reverse("goals:goal", kwargs={'id': add.id}))

    return HttpResponseRedirect(reverse("goals:index"))


def goal(request, id):
    current_user = User.objects.get(username=request.user)

    try:
        selected_goal = Goal.objects.get(pk=id)
        print(">>>> GOAL FOUND")

    except Goal.DoesNotExist:
        selected_goal = None
        print(">>>> THIS GOAL DOES NOT EXIST")
        return HttpResponseRedirect(reverse("goals:index"))

    return render(request, 'goals/goal.html', context= {
        "GoalForm": GoalForm,
        "current_user": current_user,
        "goal": selected_goal,
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