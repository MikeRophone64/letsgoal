from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Profile(models.Model):
    user                =   models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture     =   models.URLField(blank=True)
    date_of_birth       =   models.DateField(blank=True)

class Goal(models.Model):
    term_choices = [
        ("FT", "Fixed Term"), 
        ("LT", "Life-time") 
        ]
    category_choices = [
        ("FIT", "Health / Fitness"),
        ("PRO", "Career"),
        ("FIN", "Financial"),
        ("PERS", "Personal"),
        ("SPIR", "Spiritual"),
        ("FAM", "Family")
    ]
    status_choices = [
        ("NS", "Not started"),
        ("IP", "In Progress"),
        ("AC", "Accomplished")
    ]
    title               =   models.CharField(max_length=100)
    created_by          =   models.ForeignKey(User, on_delete=models.CASCADE)
    created_at          =   models.DateField(auto_now=True)
    updated_at          =   models.DateField(auto_now=True)
    term                =   models.CharField(max_length=50, choices=term_choices)
    deadline            =   models.DateField()
    category            =   models.CharField(max_length=50, choices=category_choices)
    description         =   models.TextField(max_length=140, blank=True)
    purpose             =   models.TextField(max_length=140, blank=True)
    status              =   models.CharField(max_length=50, choices=status_choices, default=status_choices[1][1])
    private             =   models.BooleanField(default=False)
    likes               =   models.ManyToManyField(User, default=None, blank=True, related_name="users_like")
    support             =   models.ManyToManyField(User, blank=True,  related_name="users_support")
    copied_by           =   models.ManyToManyField(User, blank=True,  related_name="users_copies")
    # origin              =   models.ForeignKey("self")


    def __str__(self):
        return f"{self.created_by} - {self.title}"

    @property
    def num_likes(self):
        return self.likes.all().count()

    @property
    def num_supports(self):
        return self.support.all().count()

    @property
    def num_copies(self):
        return self.copied_by.all().count()

    @property
    def trending(self):
        top_five = Goal.objects.all().order_by('-likes')[:1]
        if self in top_five:
            return True
        return False


class Like(models.Model):
    liked_by            =   models.ForeignKey(User, on_delete=models.CASCADE)
    liked_goal          =   models.ForeignKey(Goal, on_delete=models.CASCADE)
    liked_at            =   models.DateField(auto_now=True)
