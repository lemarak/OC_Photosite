# users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileUserPageView(LoginRequiredMixin, UpdateView):
    """Display update page."""
    model = get_user_model()
    login_url = reverse_lazy('login')
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'registration/profile.html'

    def get_object(self, queryset=None):
        user = get_user_model()
        return user.objects.get(id=self.request.user.id)
