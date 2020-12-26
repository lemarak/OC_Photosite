"""Test the View module for gallery."""


from datetime import datetime, date

from PIL import Image
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from gallery.models import Category, Picture
from gallery.views import (
    home_view,
    PictureDisplayView,
    GalleryListView,
    CategoryListView,
)


class BaseViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture."""
        super(BaseViewTestCase, cls).setUpClass()

        # create user
        User = get_user_model()
        cls.user = User.objects.create(
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
        for indice in range(1, 9):
            cls.picture = Picture(
                title='test_title_%s' % indice,
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

        # create categories
        for indice in range(1, 6):
            cls.category = Category(
                name="category_test_%s" % indice,
                in_menu=True,
                order_menu=1
            )
            cls.category.save()
            cls.pictures[0].categories.add(cls.category)

        cls.client_login = Client(HTTP_REFERER=reverse('gallery:home'))
        cls.logged_in = cls.client_login.login(
            username='test', password='123test')


class GalleryViewTestCase(BaseViewTestCase):
    """Class to test the display of categories."""

    def test_categories_list(self):
        """ test display categories """

        url = reverse('gallery:categories')
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['categories']) == 5)
        self.assertInHTML("category_test_1", html)

    def test_gallery_logged_in_user(self):
        """ test gallery logged in user pictures """
        url = reverse('gallery:pictures_list', args=['user'])
        response = self.client_login.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.logged_in)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("Photos de test", html)

    def test_lists_all_pictures_from_logged_in_user(self):
        """ test gallery logged in user pictures, page 2 """
        url = reverse('gallery:pictures_list', args=['user'])
        response = self.client_login.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['pictures']) == 2)

    def test_gallery_user(self):
        """ test gallery user pictures """
        url = reverse('gallery:pictures_list', args=['user', 1])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("Photos de test", html)

    def test_gallery_all_pictures_user(self):
        """ test gallery user pictures, page 2 """
        url = reverse('gallery:pictures_list', args=['user', 1])
        response = self.client.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 2)

    def test_gallery_last(self):
        """ test gallery last pictures """
        url = reverse('gallery:pictures_list', args=['last'])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("Les dernières photos déposées", html)

    def test_gallery_all_pictures_last(self):
        """ test gallery last pictures, page 2 """
        url = reverse('gallery:pictures_list', args=['last'])
        response = self.client.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 2)

    def test_gallery_categories(self):
        """ test gallery categories pictures """
        url = reverse('gallery:pictures_list', args=['category', 1])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 1)
        self.assertInHTML("Photos de category_test_1", html)
