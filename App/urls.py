from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.custom_logout, name="logout"),
    path("setting", views.setting, name="setting"),
    path("upload", views.upload, name="upload"),
    path("search", views.search, name="search"),
    path("likepost", views.likepost, name="likepost"),
    path("follow", views.follow, name="follow"),
    path("profile/<str:pk>/", views.profile, name="profile"),
]
