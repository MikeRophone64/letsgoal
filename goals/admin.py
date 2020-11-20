from django.contrib import admin
from .models import User, Profile, Goal, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Goal)
admin.site.register(Like)
