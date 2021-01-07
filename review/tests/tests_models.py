""" models for app review """

from datetime import datetime, date

from django.test import TestCase
from django.contrib.auth import get_user_model

from review.models import Review
from gallery.models import Picture


class BaseModelTestCase(TestCase):
    """ class SetUp """
    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture."""
        super(BaseModelTestCase, cls).setUpClass()

        # create user
        cls.User = get_user_model()
        cls.user = cls.User.objects.create(
            username='test',
            email='test@example.com',
            password='123test'
        )

        cls.picture = Picture(
            title='test_title',
            # file_name=image_file,
            description='test_description',
            technical='test_technical',
            camera='test_camera',
            place='test_place',
            taken_date=date(2021, 1, 1),
            # global_score = 0,
            user=cls.user,
            upload_date=datetime.now(),
        )
        cls.picture.save()

        cls.review = Review(
            score_intention=4,
            score_technical=4,
            score_picture=5,
            score_global=5,
            comment_intention="comment_intention",
            comment_technical="comment_technical",
            comment_picture="comment_picture",
            comment_global="comment_global",
            picture=cls.picture,
            user=cls.user
        )

        cls.review.save()

        cls.picture.save()


class ReviewModelTestCase(BaseModelTestCase):
    """Class to test the creation of reviews."""

    def test_create_review(self):
        """test review creation."""
        self.assertEqual(self.review.comment_intention, "comment_intention")

    def test_calculate_note_review(self):
        """ unit test for calculate_note_review """
        result = Review.objects.calculate_note_review(self.review)
        self.assertEqual(result, 4.5)

    def test_update_note_reviews(self):
        """ unit test for calculate_note_review """
        result = Review.objects.update_note_reviews(
            self.review.picture)
        self.assertEqual(result, 4.5)

    def test_calculate_note_review_after_update(self):
        """ unit test for update_note_reviews """
        self.review.score_picture = 4
        self.review.score_global = 4
        self.review.save()
        self.assertEqual(self.review.calculated_score, 4)

    def test_update_note_reviews_after_update(self):
        """ unit test for update_note_reviews """
        self.review.score_picture = 3
        self.review.score_global = 3
        self.review.save()
        self.assertEqual(self.picture.global_score, 3.5)

    def test_update_review(self):
        """test update creation."""
        self.review.score_picture = 4
        self.review.score_global = 4
        self.review.save()
        self.assertEqual(self.review.comment_intention, "comment_intention")
        self.assertEqual(self.review.calculated_score, 4)
        self.assertEqual(self.picture.global_score, 4)
