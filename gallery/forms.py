from django import forms
from .models import Picture, Review


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        exclude = ['upload_date', 'global_score']
        widgets = {'user': forms.HiddenInput()}


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['review_date']