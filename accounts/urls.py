from django.urls import path,include
from django.contrib.auth import views as auth_views
from accounts.views import profile,SignUpView





urlpatterns = [
    path('profile/', profile, name='profile'),
    path("signup/",SignUpView.as_view(),name="signup"),
    path("",include('django.contrib.auth.urls')),
]