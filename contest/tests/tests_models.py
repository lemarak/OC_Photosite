from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, date


from contest.models import Contest
from gallery.models import Picture


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
