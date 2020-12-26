from datetime import datetime, date

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

# from django.core.files import temp as tempfile
# from django.core.files.base import File

# from PIL import Image
# from io import StringIO

from gallery.models import Category, Picture


class BaseModelTestCase(TestCase):

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

        # create category
        cls.category = Category(
            name="category_test",
            in_menu=True,
            order_menu=1
        )
        cls.category.save()

        # create pictures
        cls.pictures = []
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.picture = Picture(
            title='test_title',
            file_name=SimpleUploadedFile(name='small.gif',
                                         content=small_gif,
                                         content_type='image/gif'),
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
        cls.picture.categories.add(cls.category)


class CategoryModelTestCase(BaseModelTestCase):
    """Class to test the creation of categories."""

    def test_create_category(self):
        """test creation."""
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(self.category.name, 'category_test')
        self.assertEqual(max_length, 50)

    def test_object_category_name_is_name(self):
        """test field name is correct."""
        self.assertEqual(str(self.category), self.category.name)


class PictureModelTestCase(BaseModelTestCase):
    """Class to test the creation of pictures."""

    def test_create_picture(self):
        self.assertEqual(self.picture.global_score, 0)

    def test_picture_category(self):
        """Tests the association of a picture to a category."""
        self.assertTrue(self.category in self.picture.categories.all())

    def test_picture_user(self):
        """Tests the association of a picture to an user."""
        self.assertEqual(self.user, self.picture.user)

    def test_absolute_url_picture(self):
        """test the url from a picture """
        self.assertEqual(self.picture.get_absolute_url(),
                         '/picture/%s' % self.picture.id
                         )
