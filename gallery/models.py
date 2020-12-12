from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings

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
        verbose_name="Titre de la photo", max_length=120, help_text='Picture\'s title')
    file_name = models.ImageField(verbose_name="Fichier image")
    description = models.TextField(verbose_name="Desciption de la photo")
    technical = models.TextField(
        verbose_name="Commentaires techniques", null=True)
    camera = models.CharField(
        verbose_name="Appareil photo utilisé", max_length=200, null=True)
    lens = models.CharField(
        verbose_name="Objectif utilisé", max_length=200, null=True)
    place = models.CharField(
        verbose_name="Lieu de prise", max_length=255, null=True)
    taken_date = models.DateField(verbose_name="Date de prise", null=True)
    global_score = models.FloatField(verbose_name="Note globale", null=True)
    upload_date = models.DateTimeField(
        verbose_name="Date de téléchargement", auto_now_add=True)
    categories = models.ManyToManyField(Category)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s (%s)" % (self.title, self.file_name)


class Contest(models.Model):
    """Stores a contest"""
    title = models.CharField(
        verbose_name="Titre du concours", max_length=120, help_text='Picture\'s title')
    theme = models.CharField(
        verbose_name="Thème du concours", max_length=200, null=True)
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

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title


class Review(models.Model):
    """Stores a review"""
    score_intention = models.IntegerField(
        verbose_name="note intention", null=True)
    score_technical = models.IntegerField(
        verbose_name="note technique", null=True)
    score_picture = models.IntegerField(
        verbose_name="note photo", null=True)
    score_visual = models.IntegerField(
        verbose_name="note rendu", null=True)
    score_global = models.IntegerField(
        verbose_name="note globale", null=True)
    comment_intention = models.TextField(
        verbose_name="Commentaire intention", null=True)
    comment_technical = models.TextField(
        verbose_name="Commentaire technique", null=True)
    comment_picture = models.TextField(
        verbose_name="Commentaire photo", null=True)
    comment_visual = models.TextField(
        verbose_name="Commentaire rendu", null=True)
    comment_global = models.TextField(
        verbose_name="Commentaire global", null=True)
    calculated_score = models.FloatField(
        verbose_name="Note calculée", null=True)
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
        # unique_together = (('id_picture', 'id_contest'),)
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
        # unique_together = (('id_user', 'id_contest', 'id_picture'),)
        UniqueConstraint(fields=['id_contest_picture',
                                 'id_user'], name='id_contest_picture')
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_contest_picture = models.ForeignKey(
        'ContestPicture', on_delete=models.CASCADE)
    # id_contest = models.ForeignKey('ContestPicture', on_delete=models.CASCADE)
    score = models.IntegerField(
        verbose_name="Note pour une photo et un concours donné", null=True)
    date_score = models.DateTimeField(
        verbose_name="Date de la note", auto_now_add=True)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        pass

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s - %s" % (self.id_user, self.id_contest_picture)
