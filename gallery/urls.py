from django.urls import path
from django.views.generic.base import TemplateView
from .views import picture_upload_view, upload_success


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('image-upload', picture_upload_view, name = 'image_upload'), 
    path('upload-success', upload_success, name = 'upload_success'), 
]
