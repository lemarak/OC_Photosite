""" urls for app contest """

from django.urls import path

from .views import ContestList, ContestDetail

app_name = 'contest'

urlpatterns = [
    path('', ContestList.as_view(), name='list'),
    path('detail/<int:pk>', ContestDetail.as_view(), name='detail'),
]
