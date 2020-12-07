from django import forms
from django.db import models
from django.db.models import Count, Max
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Profile(models.Model):
    user                =   models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture     =   models.ImageField(null=True, blank=True)
    date_of_birth       =   models.DateField(null=True, blank=True)
    display_trending    =   models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}'s Profile"


class Categories(models.Model):
    name                =   models.CharField(max_length=32)
    icon                =   models.ImageField(null=True, blank=True)
    bg_picture          =   models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class GoalStatus(models.Model):
    status              =   models.CharField(max_length=32)

    def __str__(self):
        return self.status


class Goal(models.Model):
    term_choices = [
        ("FT", "Fixed Term"), 
        ("LT", "Life-time") 
        ]

    title               =   models.CharField(max_length=100)
    created_by          =   models.ForeignKey(User, on_delete=models.CASCADE)
    created_at          =   models.DateField(auto_now=True)
    updated_at          =   models.DateField(auto_now=True)
    term                =   models.CharField(max_length=50, choices=term_choices, default=term_choices[0])
    deadline            =   models.DateField()
    category            =   models.ForeignKey(Categories, on_delete=models.CASCADE)
    amount              =   models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description         =   models.TextField(max_length=140, blank=True)
    purpose             =   models.TextField(max_length=140, blank=True)
    status              =   models.ForeignKey(GoalStatus, on_delete=models.CASCADE)
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
    def is_trending(self):
        trending = Goal.objects.all().order_by('-likes')
        # trending = Goal.objects.aggregate(Max('likes'))
        print(f">>> {trending}")
        # if self == trending:
        #     return True
        return False


class Steps(models.Model):
    goal            =   models.ForeignKey(Goal, on_delete=models.CASCADE)
    title           =   models.CharField(max_length=32)
    amount          =   models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    created_at      =   models.DateTimeField(auto_now=True)
    completed       =   models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} for {self.goal}"


class Like(models.Model):
    liked_by        =   models.ForeignKey(User, on_delete=models.CASCADE)
    liked_goal      =   models.ForeignKey(Goal, on_delete=models.CASCADE)
    liked_at        =   models.DateField(auto_now=True)
