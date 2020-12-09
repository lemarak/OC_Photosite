# users/urls.py
from django.urls import path
from django.views.generic.base import TemplateView

from .views import SignUpView, UpdateUserPageView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<pk>/profile/', UpdateUserPageView.as_view(), name='profile'),
]
