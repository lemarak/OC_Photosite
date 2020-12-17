from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, date
from django.core.files import temp as tempfile
from django.core.files.base import File

from PIL import Image
from io import StringIO

from gallery.models import Category, Picture, Contest, Review, Vote


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

        # create contest
        cls.contest = Contest(
            title="Concours test",
            theme="Concours de test",
            description="Description test",
            date_begin_upload=date(2020, 12, 1),
            date_end_upload=date(2020, 12, 31),
            date_begin_vote=date(2021, 1, 1),
            date_end_vote=date(2021, 1, 31),
            date_creation=datetime.now(),
        )

        # create picture
        # size = (20, 20)
        # color = (255, 0, 0, 0)
        # img = Image.new("RGBA", size, color)
        # tempfile_io = StringIO()
        # img.save(tempfile_io, format='JPEG')
        # image_file = InMemoryUploadedFile(tempfile_io, None, 'test.jpg','image',tempfile_io.len, None)
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

class ContestModelTestCase(BaseModelTestCase):
    """Class for testing contest management."""

    def test_create_contest(self):
        """test the creation of contest."""
        max_length = self.contest._meta.get_field('title').max_length
        str_format_date = "%Y-%m-%d"
        self.assertEqual(self.contest.title, 'Concours test')
        self.assertEqual(self.contest.description, 'Description test')
        self.assertEqual(self.contest.date_begin_upload, date(2020, 12, 1))
        self.assertFalse(self.contest.archived)
        self.assertEqual(self.contest.date_creation.strftime(
            str_format_date), datetime.now().strftime(str_format_date))
        self.assertEqual(max_length, 120)


class ReviewModelTestCase(BaseModelTestCase):
    """Class to test the creation of reviews."""
    pass


class VoteModelTestCase(BaseModelTestCase):
    """Class to test the creation of votes."""
    pass
