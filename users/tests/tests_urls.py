"""test the urls."""
from django.test import SimpleTestCase
from django.urls import reverse


class UsersUrlTests(SimpleTestCase):

    def test_signup_url(self):
        """test the signup url."""
        url = reverse('signup')
        self.assertEqual(url, '/accounts/signup/')

    def test_login_url(self):
        """test the login url."""
        url = reverse('login')
        self.assertEqual(url, '/accounts/login/')

    def test_logout_url(self):
        """test the logout url."""
        url = reverse('logout')
        self.assertEqual(url, '/accounts/logout/')

    def test_profile_url(self):
        """test the profile url."""
        url = reverse('profile', args=[1234])
        self.assertEqual(url, '/accounts/1234/profile/')
