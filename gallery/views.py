"""  views for app gallery """

from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef

from review.models import Review
from contest.models import ContestPicture
from .forms import PictureForm
from .models import Picture, Category


def home_view(request):
    """  Home Page view """
    context = {'last_pictures': Picture.objects.all()[:6]}
    context['last_reviews'] = Review.objects.all()[:6]
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

    def get_context_data(self, **kwargs):
        """add reviews in global context."""
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(picture=context['picture'])
        context['reviews'] = reviews
        context['noted_by_user'] = reviews.filter(
            user=self.request.user)
        # context['noted_by_user'] = Review.objects.filter(
        #     picture=context['picture'], user=self.request.user)
        return context


class GalleryListView(ListView):
    """Display list pictures.

    **Context**
        'pictures', get by Picture.objects.filter,
    **Template:**
        'gallery/full_gallery.html'
    **parameter action:**
        - 'last': last pictures
        - 'user': user pictures
        - 'category' : pictures of one category
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
            if 'pk' in self.kwargs:
                # if other user
                user = get_user_model()
                pictures = Picture.objects.filter(
                    user=user.objects.get(pk=self.kwargs['pk']))
            else:
                # if connected user
                pictures = Picture.objects.filter(
                    user=self.request.user)
        elif self.kwargs['action'] == 'category':
            pictures = Picture.objects.filter(
                categories=Category.objects.get(pk=self.kwargs['pk']))
        return pictures

    def get_context_data(self, **kwargs):
        """add title in global context."""
        context = super().get_context_data(**kwargs)
        if self.kwargs['action'] == 'last':
            context['title'] = 'Les dernières photos déposées'
        elif self.kwargs['action'] == 'user':
            if 'pk' in self.kwargs:
                user = get_user_model()
                context['title'] = 'Photos de %s' % (
                    user.objects.get(pk=self.kwargs['pk']))
            else:
                context['title'] = 'Photos de %s' % (self.request.user)
            # for depot in contest
            context['contest'] = self.request.GET.get('for_contest', False)
            if context['contest']:
                contest_picture = ContestPicture.objects.filter(
                    picture=OuterRef('pk'), contest=context['contest'])
                context['pictures'] = context['pictures'].annotate(
                    contest_picture=Exists(contest_picture))
        else:
            context['title'] = 'Photos de %s' % (
                Category.objects.get(pk=self.kwargs['pk']))
        return context


class CategoryListView(ListView):
    """  the view for displaying the list of categories """
    model = Category
    template_name = 'gallery/categories.html'
    context_object_name = 'categories'


# Forms
def picture_upload_view(request):
    """ view upload picture """
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            picture = form.save(commit=False)
            form.save()
            return redirect(reverse('gallery:picture_detail', args=[picture.id]))
    else:
        if request.user.is_authenticated:
            form = PictureForm(initial={'user': request.user})
        else:
            return redirect('login')
    return render(request, 'gallery/form_upload_picture.html', {'form': form})
