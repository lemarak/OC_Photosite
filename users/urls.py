# users/urls.py
from django.urls import path

from .views import SignUpView, ProfileUserPageView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<pk>/profile/', ProfileUserPageView.as_view(), name='profile'),
]
