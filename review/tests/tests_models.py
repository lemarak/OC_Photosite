from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, date


from review.models import Review
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


class ReviewModelTestCase(BaseModelTestCase):
    """Class to test the creation of reviews."""
    pass


class VoteModelTestCase(BaseModelTestCase):
    """Class to test the creation of votes."""
    pass
