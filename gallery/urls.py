from django.urls import path
from django.views.generic import RedirectView

from .views import (home_view,
                    picture_upload_view,
                    GalleryListView,
                    PictureDisplayView,
                     CategoryListView,
                    )


urlpatterns = [
    path('', home_view, name='home'),
    path('pictures-gallery/<str:action>/<int:pk>',
         GalleryListView.as_view(), name='pictures_gallery'),
    path('pictures-gallery/<str:action>',
         GalleryListView.as_view(), name='pictures_gallery'),
    path('picture/<int:pk>', PictureDisplayView.as_view(), name='picture_detail'),
    path('image-upload', picture_upload_view, name='image_upload'),
    path('categories', CategoryListView.as_view(), name='categories'),
    # path('upload-success', upload_success, name='upload_success'),
    path('favicon.ico', RedirectView.as_view(
        url='/static/images/favicon.png')),
]
