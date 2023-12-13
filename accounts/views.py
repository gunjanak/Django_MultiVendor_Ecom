from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from accounts.forms import SignUpForm, LoginForm,ChangePasswordForm



# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

class MyLogoutView(LogoutView):
    next_page = '/'

class MyPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

@login_required
def profile(request):
    return render(request,'profile.html')