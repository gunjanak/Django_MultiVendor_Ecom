from django.urls import path
from profiles.views import ProfileDetailView,ProfileUpdateView

app_name = 'profiles'


urlpatterns= [
    # path('create/',ProfileCreateView.as_view(),name="profile_create"),
    path('<int:pk>/update/',ProfileUpdateView.as_view(),name="profile_update"),
    path("<int:pk>/detail/",ProfileDetailView.as_view(),name='profile_detail'),
]