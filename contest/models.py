from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import UniqueConstraint

from gallery.models import Picture


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
    deposit = models.BooleanField(
        verbose_name="Dépot photo autorisé", default=False)
    date_begin_vote = models.DateField(verbose_name="Date de début du vote")
    date_end_vote = models.DateField(verbose_name="Date de fin du vote")
    vote_open = models.BooleanField(
        verbose_name="Vote en cours", default=False)
    archived = models.BooleanField(
        verbose_name="Concours archivé", default=False)
    date_creation = models.DateTimeField(
        verbose_name="Date de création du concours", auto_now_add=True)
    contest_image = models.ImageField(
        verbose_name="Image du concours", default="#", upload_to='images/')
    pictures = models.ManyToManyField(Picture, through='ContestPicture')

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse(
            'contest:detail',
            args=[self.id]
        )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.title)


class ContestPicture(models.Model):
    """ picture uploaded for a contest """
    class Meta:
        """for primary key."""
        UniqueConstraint(
            fields=['picture', 'contest'], name='contest_picture')
        ordering = ['-date_upload']

    picture = models.ForeignKey('gallery.Picture', on_delete=models.CASCADE)
    contest = models.ForeignKey('Contest', on_delete=models.CASCADE)
    date_upload = models.DateTimeField(
        verbose_name="Date de dépot photo", auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.picture, self.contest)


class Vote(models.Model):
    """Stores a vote"""
    class Meta:
        """ define Unique constraint """
        UniqueConstraint(fields=['user',
                                 'contest',
                                 'picture'], name='contest_picture_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    contest = models.ForeignKey(
        'Contest', on_delete=models.CASCADE)
    picture = models.ForeignKey(
        'gallery.Picture', on_delete=models.CASCADE)
    score = models.IntegerField(
        verbose_name="Note pour une photo et un concours donné")
    date_score = models.DateTimeField(
        verbose_name="Date de la note", auto_now_add=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s - %s - %s" % (self.user, self.contest, self.picture)
