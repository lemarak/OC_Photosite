"""test the urls."""
from django.test import SimpleTestCase
from django.urls import reverse


class ContestUrlTests(SimpleTestCase):

    def test_url_one_contest(self):
        """test main page contest url."""
        url = reverse('contest:detail', args=[1234])
        self.assertEqual(url, '/contest/detail/1234')

    def test_url_list_contests(self):
        """test main page contest url."""
        url = reverse('contest:list')
        self.assertEqual(url, '/contest/')