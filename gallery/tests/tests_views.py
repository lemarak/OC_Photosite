"""Test the View module for gallery."""

import os
from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from gallery.models import Category, Picture


class BaseViewTestCase(TestCase):
    """ class SetUp """
    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture."""
        super(BaseViewTestCase, cls).setUpClass()

        # create user
        cls.User = get_user_model()
        cls.user = cls.User.objects.create(
            username='test',
            email='test@example.com'
        )
        cls.user.set_password('123test')
        cls.user.save()

        # create pictures
        cls.pictures = []
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.file_picture = SimpleUploadedFile(
            name='small.gif', content=cls.small_gif, content_type='image/gif')
        for indice in range(1, 9):
            cls.picture = Picture(
                title='test_title_%s' % indice,
                file_name=cls.file_picture,
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

    def test_home_not_connected(self):
        """ test home page with user not connected """
        url = reverse('gallery:home')
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<p>Vous n'êtes pas connecté</p>", html)

    def test_home_user_connected(self):
        """ test home page with user connected """
        url = reverse('gallery:home')
        response = self.client_login.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<strong>test</strong>", html)

    def test_categories_list(self):
        """ test display categories """

        url = reverse('gallery:categories')
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['categories']) == 5)
        self.assertInHTML("category_test_1 (1)", html)

    def test_gallery_user(self):
        """ test gallery user pictures """
        id_user = self.user.id
        url = reverse('gallery:pictures_list', args=['user', id_user])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("Photos de test", html)

    def test_gallery_all_pictures_user(self):
        """ test gallery user pictures, page 2 """
        id_user = self.user.id
        url = reverse('gallery:pictures_list', args=['user', id_user])
        response = self.client.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 2)

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

    def test_gallery_last(self):
        """ test gallery last pictures """
        url = reverse('gallery:pictures_list', args=['last'])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 6)
        self.assertInHTML("Galerie photo", html)

    def test_gallery_all_pictures_last(self):
        """ test gallery last pictures, page 2 """
        url = reverse('gallery:pictures_list', args=['last'])
        response = self.client.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 2)

    def test_gallery_categories(self):
        """ test gallery categories pictures """
        id_category = Category.objects.get(name='category_test_1').id
        url = reverse('gallery:pictures_list', args=['category', id_category])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['pictures']) == 1)
        self.assertInHTML("Photos de category_test_1", html)

    def test_display_picture(self):
        """ test display one picture """
        id_picture = Picture.objects.get(title='test_title_1').id
        url = reverse('gallery:picture_detail', args=[id_picture])
        response = self.client.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("test_title_1", html)

    def test_post_success_picture_upload_ok(self):
        """ test picture upload ok """
        url = reverse('gallery:image_upload')
        category = Category.objects.all()[0].id

        response = self.client_login.post(
            url, data={
                "title": 'test_upload',
                "file_name": self.file_picture,
                "description": 'description_upload',
                "camera": 'camera',
                "lens": 'lens',
                "place": 'ici',
                "taken_date": date(2021, 1, 1),
                "user": self.user,
                "categories": category,
                "upload_date": datetime.now(),
            }
        )
        self.assertEqual(response.status_code, 200)
