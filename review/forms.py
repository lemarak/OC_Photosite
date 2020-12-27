""" forms for app Review """
from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """ parameters of review form """
    class Meta:
        """ fields and widgets of review form """
        model = Review
        fields = (
            'score_intention',
            'comment_intention',
            'score_technical',
            'comment_technical',
            'score_picture',
            'comment_picture',
            'score_global',
            'comment_global',
        )
        widgets = {
            # 'score_intention': forms.RadioSelect(),
            'comment_intention': forms.Textarea(attrs={
                'rows': '2',
                'placeholder': """La compréhension de l\'intention du photographe
                        (objective et subjective)..."""}),
            'comment_technical': forms.Textarea(attrs={
                'rows': '2',
                'placeholder': """Maitrise technique (cadrage, choix Iso, ouverture, traitement N&B,
                            gestion des couleurs...). Subjectif..."""}),
            'comment_picture': forms.Textarea(attrs={
                'rows': '2',
                'placeholder': """Principalement la composition et le cadrage.
                        L\'appréciation est à la fois objective et subjective..."""}),
            'comment_global': forms.Textarea(attrs={
                'rows': '2',
                'placeholder': 'Impression générale...'})
        }
