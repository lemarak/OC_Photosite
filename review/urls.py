from django.urls import path
from django.views.generic import RedirectView

from .views import (
    ReviewDetail,
    ReviewList,
    ReviewCreate,
)

app_name = 'review'

urlpatterns = [
    path('detail/<int:pk>', ReviewDetail.as_view(), name='detail'),
    path('list', ReviewList.as_view(), name='list' ),
    path('create/<int:pk>', ReviewCreate.as_view(), name='review_create'),
]
