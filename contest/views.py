""" views for app contest """

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator

from gallery.models import Picture
from .models import Contest, ContestPicture, Vote

# Create your views here.


class ContestList(ListView):
    """ list all contests """
    model = Contest
    template_name = 'contest/contest_list.html'
    context_object_name = 'contests'

    def get_context_data(self, **kwargs):
        """add title in global context."""
        context = super().get_context_data(**kwargs)
        context['contest_deposit'] = Contest.objects.filter(
            deposit=True
        )
        context['contest_vote'] = Contest.objects.filter(
            vote_open=True
        )
        context['contest_archived'] = Contest.objects.filter(
            archived=True,
        ).order_by('-date_end_vote')
        return context


def contest_detail_view(request, pk_contest):
    """ get the detail page of a contest
    with its pictures gallery """
    # get context
    contest = get_object_or_404(Contest, pk=pk_contest)
    context = {'contest': contest}
    pictures = contest.pictures.all()
    context['pictures'] = pictures

    # pagination
    paginator = Paginator(pictures, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['paginator'] = paginator
    context['page_obj'] = page_obj

    return render(request, 'contest/contest_detail.html', context)


def user_vote(request, pk_contest, pk_picture):
    """ User vote for a picture """
    if request.user.is_authenticated:

        Vote.objects.get_or_create(
            user=request.user,
            contest=Contest.objects.get(pk=pk_contest),
            picture=Picture.objects.get(pk=pk_picture),
            score=1
        )

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('login')
