from django.db import models
from django.db.models import UniqueConstraint
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

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


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
        Category, null=True, blank=True, default="")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def get_absolute_url(self):
        """get url page from a picture."""
        return reverse(
            'picture_detail',
            args=[self.id]
        )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s (%s)" % (self.title, self.file_name)

    class Meta:
        ordering = ['-upload_date']


class Contest(models.Model):
    """Stores a contest"""
    title = models.CharField(
        verbose_name="Titre du concours", max_length=120, help_text='Picture\'s title')
    theme = models.CharField(
        verbose_name="Thème du concours", max_length=200, null=True, default="")
    description = models.TextField(verbose_name="Desciption du concours")
    date_begin_upload = models.DateField(
        verbose_name="Date de début dépot photo")
    date_end_upload = models.DateField(verbose_name="Date de fin dépot photo")
    date_begin_vote = models.DateField(verbose_name="Date de début du vote")
    date_end_vote = models.DateField(verbose_name="Date de fin du vote")
    archived = models.BooleanField(
        verbose_name="Concours archivé", default=False)
    date_creation = models.DateTimeField(
        verbose_name="Date de création du concours", auto_now_add=True)
    contest_image = models.ImageField(
        verbose_name="Image du concours", default="#", upload_to='images/')

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title


class Review(models.Model):
    """Stores a review"""
    score_intention = models.IntegerField(
        verbose_name="note intention", blank=True, default=-1)
    score_technical = models.IntegerField(
        verbose_name="note technique", blank=True, default=-1)
    score_picture = models.IntegerField(
        verbose_name="note photo", blank=True, default=-1)
    score_visual = models.IntegerField(
        verbose_name="note rendu", blank=True, default=-1)
    score_global = models.IntegerField(
        verbose_name="note globale", blank=True, default=-1)
    comment_intention = models.TextField(
        verbose_name="Commentaire intention", blank=True, default=-1)
    comment_technical = models.TextField(
        verbose_name="Commentaire technique", blank=True, default=-1)
    comment_picture = models.TextField(
        verbose_name="Commentaire photo", blank=True)
    comment_visual = models.TextField(
        verbose_name="Commentaire rendu", blank=True)
    comment_global = models.TextField(
        verbose_name="Commentaire global", blank=True)
    calculated_score = models.FloatField(
        verbose_name="Note calculée", blank=True)
    review_date = models.DateTimeField(
        verbose_name="Date de la critique", auto_now_add=True)
    picture = models.ForeignKey('Picture', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s - %s" % (self.picture, self.user)


class ContestPicture(models.Model):
    class Meta:
        """for primary key."""
        UniqueConstraint(
            fields=['id_picture', 'id_contest'], name='id_contest_picture')

    id_picture = models.ForeignKey('Picture', on_delete=models.CASCADE)
    id_contest = models.ForeignKey('Contest', on_delete=models.CASCADE)
    date_upload = models.DateTimeField(
        verbose_name="Date de dépot photo", auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.id_picture, self.id_contest)


class Vote(models.Model):
    """Stores a vote"""
    class Meta:
        UniqueConstraint(fields=['id_contest_picture',
                                 'id_user'], name='id_contest_picture_user')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_contest_picture = models.ForeignKey(
        'ContestPicture', on_delete=models.CASCADE)
    score = models.IntegerField(
        verbose_name="Note pour une photo et un concours donné")
    date_score = models.DateTimeField(
        verbose_name="Date de la note", auto_now_add=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s - %s" % (self.id_user, self.id_contest_picture)
