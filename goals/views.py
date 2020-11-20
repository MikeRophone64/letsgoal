import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from .models import User, Profile, Goal, Like



# Create your views here.
@login_required(login_url='/goals/login/')
def index(request):

    goals = Goal.objects.all()
    return render(request, 'goals/index.html', context= {
        "goals": goals
    })


def register(request):
    pass


def login(request):
    pass