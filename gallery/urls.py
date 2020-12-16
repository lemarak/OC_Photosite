from django.urls import path
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

from .views import home_view, picture_upload_view, upload_success, GalleryListView


urlpatterns = [
    path('', home_view, name='home'),
    path('image-upload', picture_upload_view, name = 'image_upload'),
    path('upload-success', upload_success, name = 'upload_success'),
    path('pictures-gallery', GalleryListView.as_view(), name = 'pictures_gallery'),
    path('favicon.ico',RedirectView.as_view(url='/static/images/favicon.png')),
]
