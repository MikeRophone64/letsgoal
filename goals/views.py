import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from .models import User, Profile, Goal, Like, GoalStatus
from .forms import GoalForm, UserForm, ProfileForm

from .error import catch


# ==================================================== INDEX VIEW
@login_required(login_url="goals:login")
def index(request):
    current_user = User.objects.get(username=request.user)
    all_goals = Goal.objects.all()
    goals = Goal.objects.filter(created_by=current_user)
    
    # for goal in all_goals:
    #     if goal.is_trending == True:
    #         trending_goal = goal

    # Paginator
    p = Paginator(goals, 4)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)

    return render(request, 'goals/index.html', context= {
        "current_user": current_user,
        "GoalForm": GoalForm,
        "goals": page,
        # "trending_goal": trending_goal,
    })


# ==================================================== CREATE NEW GOAL
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


# ==================================================== DELETE A GOAL
@login_required(login_url="goals:login")
def delete_goal(request, id):
    goal_to_delete = Goal.objects.get(pk=id)
    goal_to_delete.delete()
    
    return HttpResponseRedirect(reverse("goals:index"))


# ==================================================== GOAL VIEW
@login_required(login_url="goals:login")
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


# ==================================================== USER PROFILE
@login_required(login_url="goals:login")
def profile(request, username):

    if request.method == 'POST':
        pass


    # if no profile exists, create one 
    try:
        current_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.info(request, "This profile dos not exist...", extra_tags="danger")
        return HttpResponseRedirect(reverse("goals:index"))

    user_profile = Profile.objects.get_or_create(user=current_user)

    # populate Forms 
    uf_data = {'username': current_user.username, 'email': current_user.email, 
                'password': current_user.password,}
    pf_data = {'date_of_birth': current_user.profile.date_of_birth}
    user_form = UserForm(initial=uf_data)
    profile_form = ProfileForm(initial=pf_data)

    return render(request, 'goals/user_profile.html', context= {
        'current_user': current_user,
        'UserForm': user_form,
        'ProfileForm': profile_form,
    })


# ==================================================== REGISTER VIEW
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
        return HttpResponseRedirect('goals:index')

    return render(request, 'goals/register.html')


# ==================================================== LOGIN VIEW
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