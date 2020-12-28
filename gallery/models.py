from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from users.models import CustomUser


class Category(models.Model):
    """Stores a category"""
    name = models.CharField(verbose_name="Nom de la catégorie",
                            max_length=50, help_text='Category\'s name')
    creation_date = models.DateTimeField(
        verbose_name="Date de création", auto_now_add=True)
    in_menu = models.BooleanField(
        verbose_name="Catégorie apparait dans menu", default=False)
    order_menu = models.IntegerField(
        verbose_name="Ordre d'apparition dans menu", default=0)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.name)


# Picture
class Picture(models.Model):
    """Stores a picture"""
    title = models.CharField(
        verbose_name="Titre de la photo", max_length=120, help_text=_('Picture\'s title'))
    file_name = models.ImageField(
        verbose_name="Fichier image", upload_to='images/')
    description = models.TextField(verbose_name="Desciption de la photo")
    technical = models.TextField(
        verbose_name="Commentaires techniques", null=True, blank=True, default="")
    camera = models.CharField(
        verbose_name="Appareil photo utilisé", max_length=200, null=True, blank=True, default="")
    lens = models.CharField(
        verbose_name="Objectif utilisé", max_length=200, null=True, blank=True, default="")
    place = models.CharField(
        verbose_name="Lieu de prise", max_length=255, null=True, blank=True, default="")
    taken_date = models.DateField(
        verbose_name="Date de prise", null=True, blank=True, default="")
    global_score = models.FloatField(
        verbose_name="Note globale", null=True, blank=True, default=0)
    upload_date = models.DateTimeField(
        verbose_name="Date de téléchargement", auto_now_add=True)
    categories = models.ManyToManyField(
        Category)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def get_absolute_url(self):
        """get url page from a picture."""
        return reverse(
            'gallery:picture_detail',
            args=[self.id]
        )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s (%s)" % (self.title, self.file_name)

    class Meta:
        ordering = ['-upload_date']
