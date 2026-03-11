from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
    path("profile/", views.profile, name="profile"),
]
