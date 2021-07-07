from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from accounts.models import User
from .forms import LoginForm
# Create your views here.
class LoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"