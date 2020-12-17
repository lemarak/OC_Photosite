from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView

from .forms import PictureForm
from .models import Picture, Category


def home_view(request):
    last_pictures = Picture.objects.all()[:6]
    context = {'last_pictures': last_pictures}
    if request.user.is_authenticated:
        user_pictures = Picture.objects.filter(user=request.user)[:6]
        context['user_pictures'] = user_pictures
    return render(request, 'home.html', context)


def picture_upload_view(request):
    """ view upload picture """
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        if request.user.is_authenticated:
            form = PictureForm(initial={'user': request.user})
        else:
            return redirect('login')
    return render(request, 'gallery/form_upload_picture.html', {'form': form})


def upload_success(request):
    return HttpResponse('Téléchargement réussi')


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
    template_name = 'gallery/picture.html'


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
            context['title'] = 'Photos de %s' %(self.request.user)
        return context