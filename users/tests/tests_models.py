from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):
    """tests users application."""

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        """Tests the creation of a user."""

        user = self.User.objects.create(
            username='test',
            email='test@example.com',
            password='123test',
            city='Rennes',  # Field created for the application
            biography='Ma biographie'  # Field created for the application
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.city, 'Rennes')
        self.assertEqual(user.biography, 'Ma biographie')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Tests the creation of a super user."""

        superUser = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='123test',
        )
        self.assertEqual(superUser.username, 'admin')
        self.assertEqual(superUser.email, 'admin@example.com')
        self.assertTrue(superUser.is_active)
        self.assertTrue(superUser.is_superuser)