""" urls from app review """

from django.urls import path

from .views import (
    ReviewDetail,
    ReviewList,
    ReviewCreate,
    ReviewUpdate,
    ReviewDelete
)

app_name = 'review'

urlpatterns = [
    path('detail/<int:pk>', ReviewDetail.as_view(), name='detail'),
    path('list', ReviewList.as_view(), name='list'),
    path('create/<int:pk_picture>', ReviewCreate.as_view(), name='review_create'),
    path('update/<int:pk>', ReviewUpdate.as_view(), name='review_update'),
    path('delete/<int:pk>', ReviewDelete.as_view(), name='review_delete'),
]
