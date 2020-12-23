from django import forms

from .models import Picture


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        exclude = ['upload_date', 'global_score']
        widgets = {'user': forms.HiddenInput()}


