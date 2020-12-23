from django.urls import path
from django.views.generic import RedirectView

from .views import (
    ReviewDetail,
    ReviewCreate,
)

urlpatterns = [
    path('<int:pk>', ReviewDetail.as_view(), name='review'),
    path('create/<int:pk>', ReviewCreate.as_view(), name='review_create'),
]
