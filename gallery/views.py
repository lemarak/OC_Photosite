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


def picture_display_view(request):
    pass


class GalleryListView(ListView):
    """Display list pictures for a logged user.

    **Context**
        'pictures', get by Picture.objects.filter,
    **Template:**
        'products/favorites.html'
    """

    model = Picture
    template_name = 'gallery/full_gallery.html'
    context_object_name = 'pictures'
    paginate_by = 6
