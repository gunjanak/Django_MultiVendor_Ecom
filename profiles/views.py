from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView,UpdateView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from profiles.models import Profile
from profiles.forms import ProfileForm


# Create your views here.
# class ProfileCreateView(LoginRequiredMixin,CreateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'profile_form.html'
#     success_url = reverse_lazy('profile_detail')

#     def form_valid(self,form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile_form.html"
    

    def get_object(self,queryset=None):
        return self.model.objects.get(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy("profiles:profile_detail",kwargs={'pk':self.request.user.profile.pk})

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = "profile_detail.html"

    def get_object(self,queryset=None):
        profile_id = self.kwargs.get('pk')
        return get_object_or_404(self.model,pk=profile_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = context['object']
        return context
    
    
    
    