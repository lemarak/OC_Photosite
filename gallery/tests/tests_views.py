"""Test the View module for gallery."""

from PIL import Image
from datetime import datetime, date
from io import StringIO

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
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
        cls.User = get_user_model()
        cls.user = cls.User.objects.create(
            username='test',
            email='test@example.com',
            password='123test'
        )

        # create pictures
        cls.pictures = []
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        for indice in range(1, 8):
            cls.picture = Picture(
                title='test_title_%s' % indice,
                file_name=SimpleUploadedFile(name='small.gif', content=small_gif, content_type='image/gif'),
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

    def test_gallery_last(self):
        """ test gallery last pictures """
        url = reverse('gallery:pictures_list', args=['last'])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("test_description", html)

    def test_gallery_user(self):
        """ test gallery last pictures """
        url = reverse('gallery:pictures_list', args=['user'])
        response = self.client_login.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("test_description", html)
