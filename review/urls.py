from django.urls import path
from django.views.generic import RedirectView

from .views import (
    ReviewDetail,
    ReviewCreate,
)

app_name = 'review'

urlpatterns = [
    path('', ReviewDetail.as_view(), name=''), # to update
    path('detail/<int:pk>', ReviewDetail.as_view(), name='detail'),
    path('create/<int:pk>', ReviewCreate.as_view(), name='review_create'),
]
