"""Test the View module for review."""

from datetime import datetime, date

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model

from review.models import Review
from gallery.models import Picture


class BaseViewTestCase(TestCase):
    """ Set up """
    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture."""
        super(BaseViewTestCase, cls).setUpClass()

        # create user
        cls.user = get_user_model().objects.create(
            username='test',
            email='test@example.com'
        )
        cls.user.set_password('123test')
        cls.user.save()

        # create pictures
        cls.pictures = []
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        cls.picture = Picture(
            title='test_title',
            file_name=SimpleUploadedFile(
                name='small.gif', content=small_gif, content_type='image/gif'),
            description='test_description',
            technical='test_technical',
            camera='test_camera',
            place='test_place',
            taken_date=date(2021, 1, 1),
            user=cls.user,
            upload_date=datetime.now(),
        )
        cls.picture.save()
        cls.pictures.append(cls.picture)

        cls.review = Review(
            score_intention=4,
            score_technical=4,
            score_picture=4,
            score_global=4,
            picture=cls.picture,
            user=cls.user
        )
        cls.review.save()

        cls.client_login = Client(HTTP_REFERER=reverse('gallery:home'))
        cls.logged_in = cls.client_login.login(
            username='test', password='123test')


# class DisplayReviewViewTests(BaseViewTestCase):
#     """  Test display review """

#     def test_display_review(self):
#         """ test display one review """
#         url = reverse('review:detail', args=[4])
#         response = self.client.get(url)
#         html = response.content.decode('utf8')
#         self.assertEqual(response.status_code, 200)
#         self.assertInHTML(
#             "Note moyenne de la revue : 4,0", html)
#         self.assertInHTML(
#             "test_title (4,00)", html)


class ReviewViewTests(BaseViewTestCase):
    """  Test form review """

    def test_display_review(self):
        """ test form review """
        id_review = self.review.id
        url = reverse('review:detail', args=[id_review])
        response = self.client_login.get(url)

        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf8')
        self.assertInHTML("Note intention : 4", html)

    def test_reviews_list(self):
        """ test display categories """

        url = reverse('review:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['reviews']) == 1)

    def test_post_success(self):
        """ test form review validation """
        id_picture = self.picture.id
        url = reverse('review:review_create', args=[id_picture])
        response = self.client_login.post(
            url, data={
                "score_intention": 4,
                "score_technical": 4,
                "score_picture": 4,
                "score_global": 4
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/review/detail/3?ok=save")

    def test_post_success_score_review_ok(self):
        """ test calculated score review after validation """
        id_picture = self.picture.id
        url = reverse('review:review_create', args=[id_picture])
        response = self.client_login.post(
            url, data={
                "score_intention": 4,
                "score_technical": 4,
                "score_picture": 4,
                "score_global": 4
            }
        )
        url = reverse('review:detail', args=[4])
        response = self.client.get(url)
        html = response.content.decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Note moyenne de la revue : 4,0", html)
