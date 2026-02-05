from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterUserForm
from django.contrib.auth.views import LoginView, LogoutView


def register_view(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ⬅️ сразу логиним после регистрации
            return redirect("index")
    else:
        form = RegisterUserForm()

    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    err_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("password") or "home"
            return redirect(next_url)
        else:
            err_message = "Invalid Credentials!"
    return render(request, "accounts/login.html", {"error": err_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    else:
        return redirect("home")


@login_required
def home_view(request):
    return render(request, "index.html")


class ProtectedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "registration/protected.html")
