from django.urls import path
from django.views.generic.base import TemplateView
from .views import home_page_view


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home')
]
