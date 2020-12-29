""" urls for app contest """

from django.urls import path

from .views import ContestList, contest_detail_view, user_vote, add_picture_to_contest

app_name = 'contest'

urlpatterns = [
    path('', ContestList.as_view(), name='list'),
    path('detail/<int:pk_contest>', contest_detail_view, name='detail'),
    path('vote/<int:pk_contest_picture>', user_vote,
         name='user_vote'),
    path('depot/<int:pk_contest>/<int:pk_picture>',
         add_picture_to_contest, name='add_picture_to_contest'),
]
