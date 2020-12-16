"""Test the View module for users."""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model, get_user
from django.urls import resolve, reverse

from users.views import SignUpView, ProfileUserPageView


class SetUp(TestCase):
    """prepare the test fixture."""
    @classmethod
    def setUpTestData(cls):
        """Method called to prepare the test fixture."""
        cls.User = get_user_model()
        cls.user_test = cls.User.objects.create_user(
            username='test',
            email='test@example.com',
            password='123test'
        )


class SignupPageTests(TestCase):

    def test_signup_view(self):
        """test route."""
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__
        )


class SigninPageTests(SetUp):
    """test signin view."""

    def test_signin_page_view(self):
        """test signin page."""
        c = Client()
        response = c.post('/accounts/login/', {
            'username': 'test',
            'password': '123test'}
        )
        user = get_user(response.wsgi_request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.username, "test")
        self.assertTrue(user.email, "test@example.com")

    def test_login_view(self):
        """test login page."""
        c = Client()
        logged_in = c.login(username='test', password='123test')
        self.assertTrue(logged_in)


class ProfilePageTests(TestCase):
    """ test profile view """

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(
            username='test2',
            email='test2@example.com',
            password='123test'
        )
        cls.client_login = Client(HTTP_REFERER=reverse('home'))
        cls.logged_in = cls.client_login.login(
            username='test2', password='123test')

    def test_profile_page(self):
        """ test page profile """

        self.assertTrue(self.user.is_authenticated)

        url = reverse('profile', args=[self.user.id])
        self.response = self.client_login.get(url)

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/profile.html')
        self.assertContains(self.response, 'Ville')
        self.assertNotContains(self.response, 'City')

    def test_profile_view(self):
        """ test view UpdateUserPageView """
        view = resolve('/accounts/1/profile/')
        self.assertEqual(
            view.func.__name__,
            ProfileUserPageView.as_view().__name__
        )
