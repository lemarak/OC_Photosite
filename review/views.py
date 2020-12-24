from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from gallery.models import Picture
from .models import Review
from .forms import ReviewForm

class ReviewDetail(DetailView):
    model = Review
    template_name = 'review/review.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super(ReviewDetail, self).get_context_data(**kwargs)
        pk_picture = context['review'].picture.id
        context['picture'] = get_object_or_404(Picture, pk=pk_picture)
        return context


# Create review
class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/form_review.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        user = self.request.user
        review.user = user
        picture = get_object_or_404(Picture, pk=self.kwargs['pk'])
        review.picture = picture
        # calculate note
        review.calculated_score = Review.objects.calculate_note_review(review)
        review.save()
        picture.global_score = Review.objects.update_note_reviews(
            picture, review.calculated_score)
        picture.save()
        return HttpResponseRedirect(reverse('review:detail', args=[review.id]))

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data(**kwargs)
        context['picture'] = get_object_or_404(Picture, pk=self.kwargs['pk'])
        return context
