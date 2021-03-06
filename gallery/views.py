"""  views for app gallery """

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef

from taggit.models import Tag
from review.models import Review
from contest.models import ContestPicture, Contest
from .forms import PictureForm
from .models import Picture, Category


def home_view(request):
    """  Home Page view """
    context = {'last_pictures': Picture.objects.all()[:6]}
    context['last_reviews'] = Review.objects.all()[:6]
    if request.user.is_authenticated:
        user_pictures = Picture.objects.filter(user=request.user)[:6]
        context['user_pictures'] = user_pictures
    context['contests'] = Contest.objects.all().order_by('-date_creation')[:3]
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
    template_name = 'gallery/detail.html'

    def get_context_data(self, **kwargs):
        """add reviews in global context."""
        context = super().get_context_data(**kwargs)
        picture = context['picture']
        reviews = Review.objects.filter(picture=picture)

        context['reviews'] = reviews
        if self.request.user.is_authenticated:
            context['noted_by_user'] = reviews.filter(
                user=self.request.user)

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
        order_by = self.request.GET.get('order_by', '-upload_date')
        if self.kwargs['action'] == 'last':
            # last pictures
            pictures = Picture.objects.all().order_by(order_by)

        elif self.kwargs['action'] == 'user':
            # user
            if 'pk' in self.kwargs:
                # if other user
                user = get_user_model()
                pictures = Picture.objects.filter(
                    user=user.objects.get(pk=self.kwargs['pk'])
                ).order_by(order_by)
            elif self.request.user.is_authenticated:
                # if connected user
                pictures = Picture.objects.filter(
                    user=self.request.user)
        elif self.kwargs['action'] == 'category':
            # category
            pictures = Picture.objects.filter(
                categories=Category.objects.get(pk=self.kwargs['pk'])
            ).order_by(order_by)
        elif self.kwargs['action'] == 'tag':
            # tag
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            pictures = Picture.objects.filter(
                tags__in=[tag]
            )
        return pictures

    def get_context_data(self, **kwargs):
        """add title in global context."""
        context = super().get_context_data(**kwargs)
        context['action'] = self.kwargs['action']
        if self.kwargs['action'] == 'last':
            context['title'] = 'Galerie photo'

        elif self.kwargs['action'] == 'user':
            if 'pk' in self.kwargs:
                user = get_user_model()
                user_request = user.objects.get(pk=self.kwargs['pk'])
                context['title'] = 'Photos de %s' % (user_request)
                context['user_id'] = user_request.id
            else:
                context['title'] = 'Photos de %s' % (self.request.user)
                context['user_id'] = self.request.user.id
            # for depot in contest
            context['contest'] = self.request.GET.get('for_contest', False)
            if context['contest']:
                contest_picture = ContestPicture.objects.filter(
                    picture=OuterRef('pk'), contest=context['contest'])
                context['pictures'] = context['pictures'].annotate(
                    contest_picture=Exists(contest_picture))
        elif self.kwargs['action'] == 'category':
            context['title'] = 'Photos de %s' % (
                Category.objects.get(pk=self.kwargs['pk']))
            context['category_id'] = self.kwargs['pk']
        elif self.kwargs['action'] == 'tag':
            context['title'] = 'Photos avec le tag %s' % (
                get_object_or_404(Tag, slug=self.kwargs['tag_slug']).name)
            
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
