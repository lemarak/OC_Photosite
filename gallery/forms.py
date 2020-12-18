from django import forms
from django.utils.safestring import mark_safe

from .models import Picture, Review


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        exclude = ['upload_date', 'global_score']
        widgets = {'user': forms.HiddenInput()}


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = (
            'score_intention',
            'comment_intention',
            'score_technical',
            'comment_technical',
            'score_picture',
            'comment_picture',
            'score_visual',
            'comment_visual',
            'score_global',
            'comment_global',
        )
        widgets = {
            # 'score_intention': forms.RadioSelect(),
            'comment_intention': forms.Textarea(attrs={'rows': '3'}),
            'comment_technical': forms.Textarea(attrs={'rows': '3'}),
            'comment_picture': forms.Textarea(attrs={'rows': '3'}),
            'comment_visual': forms.Textarea(attrs={'rows': '3'}),
            'comment_global': forms.Textarea(attrs={'rows': '3'})
        }
