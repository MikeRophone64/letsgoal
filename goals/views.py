import datetime
from django.shortcuts import render, HttpResponse
from .models import User, Profile, Goal, Like



# Create your views here.
def index(request):

    goals = Goal.objects.all()
    return render(request, 'goals/index.html', context= {
        "goals": goals
    })