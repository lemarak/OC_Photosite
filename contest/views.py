""" views for app contest """

from datetime import date, datetime

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView


from .models import Contest

# Create your views here.

class ContestList(ListView):
    """ list all contests """
    model = Contest
    template_name = 'contest/contest_list.html'
    context_object_name = 'contests'

    def get_context_data(self, **kwargs):
        """add title in global context."""
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['contest_deposit']=Contest.objects.filter(
            date_begin_upload__lte=today,
            date_end_upload__gte=today,
            )
        context['contest_vote']=Contest.objects.filter(
            date_begin_vote__lte=today,
            date_end_vote__gte=today,
            )
        context['contest_archived']=Contest.objects.filter(
            date_end_vote__lte=today,
            ).order_by('-date_end_vote')
        print('*** context ***', context)
        return context


class ContestDetail(DetailView):
    model = Contest
    template_name = 'contest/contest_detail.html'
    context_object_name = 'contest'
