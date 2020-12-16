from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PictureForm


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
