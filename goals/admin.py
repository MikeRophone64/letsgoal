from django.contrib import admin
from .models import User, Profile, Categories, GoalStatus, Goal, Like, Steps

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Categories)
admin.site.register(GoalStatus)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_by', 'term', 'category', 'status', 'num_likes',]

@admin.register(Steps)
class StepsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'completed']

admin.site.register(Like)
