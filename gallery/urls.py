from django.urls import path
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

from .views import (home_view,
                    picture_upload_view,
                    upload_success,
                    GalleryListView,
                    PictureDisplayView,
                    ReviewDetail,
                    ReviewCreate,
                    )


urlpatterns = [
    path('', home_view, name='home'),
    path('pictures-gallery/<str:action>', GalleryListView.as_view(), name='pictures_gallery'),
    path('picture/<int:pk>', PictureDisplayView.as_view(), name='picture_detail'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review'),
    path('review/create/<int:pk>', ReviewCreate.as_view(), name='review_create'),
    path('image-upload', picture_upload_view, name='image_upload'),
    path('upload-success', upload_success, name='upload_success'),
    path('favicon.ico', RedirectView.as_view(
        url='/static/images/favicon.png')),
]
