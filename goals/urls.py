from django.urls import path
from . import views
import goals.api_views

from django.conf.urls.static import static
from django.conf import settings

app_name = "goals"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("goal/<int:id>", views.goal, name="goal"),
    path("profile/<str:username>", views.profile, name="profile"),

    # API views
    # path("api/v1/goals/", goals.api_views.GoalList.as_view()),
    path("new_goal", views.new_goal, name="new_goal"),
    path("delete_goal/<int:id>", views.delete_goal, name="delete_goal"),
    # path("api/v1/goals/<int:id>/", goals.api_views.GoalRetrieveUpdateDestroy.as_view()),
] 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)