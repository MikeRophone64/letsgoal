from django.contrib import admin
from .models import User, Profile, Categories, GoalStatus, Goal, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Categories)
admin.site.register(GoalStatus)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'term', 'category', 'status']

admin.site.register(Like)
