import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from .models import User, Categories, Profile, Goal, Like, GoalStatus, Steps
from .forms import GoalForm, UserForm, ProfileForm, GoalStepForm

from .error import catch


# ==================================================== INDEX VIEW
@login_required(login_url="goals:login")
def index(request):
    current_user = User.objects.get(username=request.user)
    all_goals = Goal.objects.all()
    goals = Goal.objects.filter(created_by=current_user)

    trending_goal = Goal.objects.annotate(all_likes=Count('likes')).order_by('-all_likes')[0]

    return render(request, 'goals/index.html', context= {
        'current_user': current_user,
        'GoalForm': GoalForm,
        'goals': goals,
        'trending_goal': trending_goal,
    })


# ==================================================== TRENDING GOALS VIEW
@login_required(login_url="goals:login")
def trending_goals(request):
    current_user = User.objects.get(username=request.user)
    trending = Goal.objects.annotate(all_likes=Count('likes')).order_by('-all_likes')

    return render(request, 'goals/trending.html', context= {
        'current_user': current_user,
        'trending': trending,
    })


# ==================================================== CREATE NEW GOAL
@login_required(login_url="goals:login")
def new_goal(request):
    current_user = User.objects.get(username=request.user)

    if request.method == "POST":
        form = GoalForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            # term = form.cleaned_data['term']
            deadline = form.cleaned_data['deadline']
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            purpose = form.cleaned_data['purpose']
            status = GoalStatus.objects.get(pk=1)
            
            add = Goal.objects.create(title=title, created_by=current_user, deadline=deadline, category=category, amount=amount, description=description, purpose=purpose, status=status)
            add.save()
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

    # if goal does not exist set it to none
    try:
        selected_goal = Goal.objects.get(pk=id)
    except Goal.DoesNotExist:
        selected_goal = None
        return HttpResponseRedirect(reverse("goals:index"))

    # find steps associated with this goal
    try:
        goal_steps = Steps.objects.filter(goal=id).order_by('-pk')

        #if goal has steps then mark goal status In Progess
        if goal_steps and selected_goal.status != GoalStatus.objects.get(pk=3):
            selected_goal.status = GoalStatus.objects.get(pk=2) # pk2 = In Progress
            selected_goal.save()

    except Steps.DoesNotExist:
        goal_steps = None

    # if financial Goal then calculate rest amount to save
    category = Categories.objects.get(name="Financial")

    if selected_goal.category == category:
        goal_amount = selected_goal.amount
        to_deduce = 0
        try:
            for step in goal_steps:
                to_deduce += step.amount
        except:
            to_deduce = 0
        
        amount_to_go = goal_amount - to_deduce
        note = f"Only {amount_to_go} to go!"
    
        if amount_to_go <= 0:
            note = "WOHOO You made it!"
            selected_goal.status = GoalStatus.objects.get(pk=3) # pk2 = Accomplished
            selected_goal.save()
    else:
        note = ''
    


    return render(request, 'goals/goal.html', context= {
        "GoalForm": GoalForm,
        "GoalStepForm": GoalStepForm,
        "current_user": current_user,
        "goal": selected_goal,
        "steps": goal_steps,
        "financial_note": note,
    })


# ==================================================== NEW GOAL STEP
def new_goal_step(request, id):
    selected_goal = Goal.objects.get(pk=id)

    if request.method == 'POST':
        form = GoalStepForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            accomplished = request.POST.get('accomplished')


            if accomplished == 'Accomplished':

                goal_done = GoalStatus.objects.get(pk=3) # 3 == accomplished
                selected_goal.status = goal_done
                selected_goal.save()

            add = Steps.objects.create(goal=selected_goal, title=title, amount=amount)


    return HttpResponseRedirect(reverse("goals:goal", kwargs={'id': id}))


# ==================================================== USER PROFILE
@login_required(login_url="goals:login")
def profile(request, username):

    # if no profile exists, create one 
    try:
        current_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.info(request, "This profile dos not exist...", extra_tags="danger")
        return HttpResponseRedirect(reverse("goals:index"))

    user_profile = Profile.objects.get_or_create(user=current_user)

    # Get user goals for stats
    user_goals = Goal.objects.filter(created_by=current_user)
    goal_accomplished = Goal.objects.filter(created_by=current_user, status=3).count()  # 3 == Accomplished
    goal_in_progress = Goal.objects.filter(created_by=current_user, status=2).count()  # 2 == In Progress
    goal_not_started = Goal.objects.filter(created_by=current_user, status=1).count()  # 1 == Not Started


    form = PasswordChangeForm(request.user)

    # populate Forms 
    uf_data = {'username': current_user.username, 'email': current_user.email, }
    pf_data = {'date_of_birth': current_user.profile.date_of_birth}
    user_form = UserForm(initial=uf_data)
    profile_form = ProfileForm(initial=pf_data)

    return render(request, 'goals/user_profile.html', context= {
        'current_user': current_user,
        'UserForm': user_form,
        'ProfileForm': profile_form,
        'form': form,
        'user_goals': user_goals,
        'accomplished': goal_accomplished,
        'inProgress': goal_in_progress,
        'notStarted': goal_not_started,
    })


# ==================================================== CHANGE PASSWORD
def update_password(request):
    current_user = User.objects.get(username=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.info(request, 'Your password was successfully updated!', extra_tags="success")
            return HttpResponseRedirect(reverse('goals:profile', kwargs={'username': current_user.username}))
        else:
            messages.info(request, 'Please correct the error below.', extra_tags="danger")
            return HttpResponseRedirect(reverse('goals:profile', kwargs={'username': current_user.username}))


# ==================================================== CHANGE PROFILE INFO
def update_profile(request):
    current_user = User.objects.get(username=request.user)

    if request.method == 'POST':
        new_username = request.POST['username']
        new_email = request.POST['email']
        new_date_of_birth = request.POST['date_of_birth']

        catch(current_user.profile.date_of_birth)

    
        current_user.username = new_username
        current_user.email = new_email
        current_user.save()

        current_user.profile.date_of_birth = new_date_of_birth
        current_user.profile.save()

        new_user = User.objects.get(username=new_username)

        messages.info(request, 'Profile updated.', extra_tags="success")
        return HttpResponseRedirect(reverse('goals:profile', kwargs={'username': current_user.username}))


# ==================================================== DISMISS TRENDING
def dismiss_trending(request):
    current_user = User.objects.get(username=request.user)

    current_user.profile.display_trending = False
    current_user.profile.save()

    messages.info(request, "Trending goals won't appear anymore", extra_tags="success")
    return HttpResponseRedirect(reverse('goals:index'))


# ==================================================== HIT LIKE
def like(request, id):
    current_user = User.objects.get(username=request.user)
    requested_goal = Goal.objects.get(pk=id)
    likes = requested_goal.likes.all()

    # If user has not liked yet => LIKE
    if current_user not in likes:
        requested_goal.likes.add(current_user)
        note = 'liked'
    else:
        # If user has already liked => UNLIKE
        requested_goal.likes.remove(current_user)
        note = 'unliked'

    updated_goal = Goal.objects.get(pk=id)

    goal_response = {
        'num_likes': updated_goal.likes.count(),
        'active_class': note,
    }
    return JsonResponse(goal_response)



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
            new_user = User.objects.create_user(username, email, password)
        except IntegrityError:
            messages.info(request, "Username already taken...", extra_tags="danger")
            return HttpResponseRedirect('register')

        # create a user profile 
        user_profile = Profile.objects.get_or_create(user=new_user)

        login(request, new_user)
        return HttpResponseRedirect(reverse('goals:index'))

    return render(request, 'goals/register.html')


# ==================================================== LOGIN VIEW
def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
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