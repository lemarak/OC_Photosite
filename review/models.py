""" models for app review """
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


# Review
class ReviewManager(models.Manager):
    """Methods associated with the Review model (calculate note)"""

    def calculate_note_review(self, instance):
        """ calculate the average score for a review """
        note_review = (instance.score_intention + instance.score_technical +
                       instance.score_picture + instance.score_global) / 4
        return note_review

    def update_note_reviews(self, picture):
        """ calculate the average review score for a picture """
        count_reviews = float(Review.objects.filter(
            picture=picture).count())
        if count_reviews > 0:
            avg_score_reviews = Review.objects.filter(
                picture=picture).aggregate(models.Avg('calculated_score'))
            return avg_score_reviews['calculated_score__avg']
        return 0


class Review(models.Model):
    """Stores a review"""
    SCORE = (
        (1, '1 - pas terrible'),
        (2, '2 - peut mieux faire'),
        (3, '3 - pas mal'),
        (4, '4 - bien'),
        (5, '5 - excellent')
    )
    score_intention = models.IntegerField(
        verbose_name="note intention",  choices=SCORE)
    score_technical = models.IntegerField(
        verbose_name="note technique",  choices=SCORE)
    score_picture = models.IntegerField(
        verbose_name="note rendu image", choices=SCORE)
    score_global = models.IntegerField(
        verbose_name="note globale", choices=SCORE)
    comment_intention = models.TextField(
        verbose_name="Commentaire intention", blank=True)
    comment_technical = models.TextField(
        verbose_name="Commentaire technique", blank=True)
    comment_picture = models.TextField(
        verbose_name="Commentaire rendu image", blank=True)
    comment_global = models.TextField(
        verbose_name="Commentaire global", blank=True)
    calculated_score = models.FloatField(
        verbose_name="Note calculée", blank=True,  default=0)
    review_date = models.DateTimeField(
        verbose_name="Date de la critique", auto_now_add=True)
    picture = models.ForeignKey('gallery.Picture', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    # Manager
    objects = ReviewManager()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse(
            'review:detail',
            args=[self.id]
        )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s - %s" % (self.picture, self.user)

    class Meta:
        """ Meta for ordering """
        ordering = ['-review_date']


# method for updating review note
@receiver(pre_save, sender=Review)
def update_review_note(sender, instance, **kwargs):
    """ save review note """
    instance.calculated_score = Review.objects.calculate_note_review(instance)


# method for updating picture note
@receiver(post_save, sender=Review)
def update_picture_note(sender, instance, **kwargs):
    """ save picture note """
    instance.picture.global_score = Review.objects.update_note_reviews(
        instance.picture)
    instance.picture.save()


# method for updating picture note when review deleted
@receiver(post_delete, sender=Review)
def update_picture_note_when_delete(sender, instance, **kwargs):
    """ save picture note """
    instance.picture.global_score = Review.objects.update_note_reviews(
        instance.picture)
    instance.picture.save()
