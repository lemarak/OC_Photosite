from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PictureForm, ReviewForm
from .models import Picture, Category, Review


def home_view(request):
    last_pictures = Picture.objects.all()[:6]
    context = {'last_pictures': last_pictures}
    if request.user.is_authenticated:
        user_pictures = Picture.objects.filter(user=request.user)[:6]
        context['user_pictures'] = user_pictures
    return render(request, 'home.html', context)


class PictureDisplayView(DetailView):
    """Display an individual picture.

    **Context**
    ''picture''
        An instance of :model:`gallery.Picture`.

    **Template:**
        'gallery/picture.html'
    """
    model = Picture
    context_object_name = 'picture'
    template_name = 'gallery/display_picture.html'


class GalleryListView(ListView):
    """Display list pictures.

    **Context**
        'pictures', get by Picture.objects.filter,
    **Template:**
        'gallery/full_gallery.html'
    **parameter action:**
        - 'last': last pictures
        - 'user': user pictures
    """

    template_name = 'gallery/full_gallery.html'
    context_object_name = 'pictures'
    paginate_by = 6

    def get_queryset(self):
        """return pictures,
        Depends on the action parameter"""
        if self.kwargs['action'] == 'last':
            pictures = Picture.objects.all()

        elif self.kwargs['action'] == 'user':
            pictures = Picture.objects.filter(
                user=self.request.user)

        return pictures

    def get_context_data(self, **kwargs):
        """add title in global context."""
        context = super().get_context_data(**kwargs)
        if self.kwargs['action'] == 'last':
            context['title'] = 'Les dernières photos déposées'
        elif self.kwargs['action'] == 'user':
            context['title'] = 'Photos de %s' % (self.request.user)
        return context


class ReviewDetail(DetailView):
    model = Review
    template_name = 'gallery/review.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super(ReviewDetail, self).get_context_data(**kwargs)
        pk_picture = context['review'].picture.id
        context['picture'] = get_object_or_404(Picture, pk=pk_picture)
        return context


# Forms
def picture_upload_view(request):
    """ view upload picture """
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            picture=form.save(commit=False)
            form.save()
            return redirect(reverse('picture_detail', args=[picture.id]))
    else:
        if request.user.is_authenticated:
            form = PictureForm(initial={'user': request.user})
        else:
            return redirect('login')
    return render(request, 'gallery/form_upload_picture.html', {'form': form})


# def upload_success(request):
#     return HttpResponse('Téléchargement réussi')


# Review
class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'gallery/form_review.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        user = self.request.user
        review.user = user
        picture = get_object_or_404(Picture, pk=self.kwargs['pk'])
        review.picture = picture
        # calculate note
        review.calculated_score = Review.objects.calculate_note_review(review)
        review.save()
        picture.global_score = Picture.objects.update_note_reviews(
            picture, review.calculated_score)
        picture.save()
        return HttpResponseRedirect(reverse('review', args=[review.id]))

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data(**kwargs)
        context['picture'] = get_object_or_404(Picture, pk=self.kwargs['pk'])
        return context


# def picture_review_form(request, pk):
#     """ view upload picture """
#     picture = get_object_or_404(Picture, pk = pk)
#     context = {'picture': picture}
#     if request.method == 'POST':
#         form = ReviewForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             return redirect('upload_success')
#     else:
#         if request.user.is_authenticated:
#             form = ReviewForm(initial={'user': request.user, 'picture': picture})
#         else:
#             return redirect('login')
#     return render(request, 'gallery/form_review.html', {'form': form}, context=context)
