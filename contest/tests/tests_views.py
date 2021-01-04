"""Test the View module for contest."""

from datetime import datetime, date

from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from contest.models import Contest, ContestPicture
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

        # create picture
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

        # create contests vote
        cls.contest = Contest(
            title='contest_vote',
            theme='contest_theme_vote',
            description='contest_description_vote',
            date_begin_upload=date(2020, 12, 1),
            date_end_upload=date(2020, 12, 31),
            deposit=False,
            date_begin_vote=date(2021, 1, 1),
            date_end_vote=date(2021, 1, 31),
            vote_open=True,
            archived=False,
            date_creation=datetime.now(),
            contest_image=SimpleUploadedFile(
                name='small.gif', content=small_gif, content_type='image/gif'),
        )
        cls.contest.save()

        # add picture to contest
        cls.contest_picture = ContestPicture(
            picture=cls.picture,
            contest=cls.contest
        )
        cls.contest_picture.save()

        # user login
        cls.client_login = Client(HTTP_REFERER=reverse('gallery:home'))
        cls.logged_in = cls.client_login.login(
            username='test', password='123test')


class ContestViewTests(BaseViewTestCase):

    """  Test contest view """

    def test_contest_list(self):
        """ test display contest list """
        url = reverse('contest:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['contests']) == 1)

    def test_contest_detail(self):
        """ test display contest detail """
        url = reverse('contest:detail', args=[self.contest.id])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['contest_pictures']) == 1)
        self.assertInHTML("contest_vote", html)

    def test_user_vote(self):
        """ test a user's vote """
        url = reverse('contest:user_vote', args=[self.contest_picture.id])
        response = self.client_login.get(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('contest:detail', args=[self.contest.id])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("1 vote", html)

    def test_user_depot(self):
        """ test the upload of a photo by a user """
        url = reverse('contest:add_picture_to_contest', args=[
                      self.contest.id, self.picture.id])
        response = self.client_login.get(url)
        self.assertEqual(response.status_code, 302)

        url = "%s?for_contest=%s" % (reverse('gallery:pictures_list', args=[
            'user']), self.contest.id)
        response = self.client_login.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("""<button class="btn btn-secondary btn-sm" disabled>Déjà déposée</button>""", html)
