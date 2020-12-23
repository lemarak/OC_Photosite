from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint


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


class ContestPicture(models.Model):
    class Meta:
        """for primary key."""
        UniqueConstraint(
            fields=['id_picture', 'id_contest'], name='id_contest_picture')

    id_picture = models.ForeignKey('gallery.Picture', on_delete=models.CASCADE)
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
