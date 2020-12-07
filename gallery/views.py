from django.shortcuts import render
from django.http import HttpResponse


def home_page_view(request):
    return HttpResponse('Bienvenue sur le site de photos!')
