"""  views for app review """

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView

from gallery.models import Picture
from .models import Review
from .forms import ReviewForm


class ReviewDetail(DetailView):
    """ view for review detail """
    model = Review
    template_name = 'review/review.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super(ReviewDetail, self).get_context_data(**kwargs)
        pk_picture = context['review'].picture.id
        context['picture'] = get_object_or_404(Picture, pk=pk_picture)
        return context


class ReviewList(ListView):
    """list reviews """
    model = Review
    template_name = "review/gallery_reviews.html"
    context_object_name = 'reviews'
    paginate_by = 6


# Create review
class ReviewCreate(LoginRequiredMixin, CreateView):
    """ review creation form """
    model = Review
    form_class = ReviewForm
    template_name = 'review/form_review.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

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
            picture)
        picture.save()
        ok = "save"
        url = "%s?ok=%s" % (
            reverse('review:detail', args=[review.id]), ok)
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data(**kwargs)
        context['picture'] = get_object_or_404(Picture, pk=self.kwargs['pk'])
        return context


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    """ review creation form """
    model = Review
    form_class = ReviewForm
    template_name = 'review/form_review.html'
    context_object_name = 'review'

    def form_valid(self, form):
        # calculate note
        review = form.save(commit=False)
        review.calculated_score = Review.objects.calculate_note_review(review)
        review.save()
        review.picture.global_score = Review.objects.update_note_reviews(
            review.picture)
        review.picture.save()
        ok = "save"
        url = "%s?ok=%s" % (
            reverse('review:detail', args=[review.id]), ok)
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super(ReviewUpdate, self).get_context_data(**kwargs)
        context['picture'] = context['review'].picture
        return context


class ReviewDelete(LoginRequiredMixin, DeleteView):
    """ delete a review """
    model = Review

    def get_success_url(self):
        """ succes url """
        picture = self.object.picture
        return reverse_lazy('gallery:picture_detail', args=[picture.id])

