"""test the urls."""
from django.test import SimpleTestCase
from django.urls import reverse


class ContestUrlTests(SimpleTestCase):

    def test_url_one_contest(self):
        """test main page contest url."""
        url = reverse('contest:detail', args=[1234])
        self.assertEqual(url, '/contest/detail/1234')

    def test_url_list_contests(self):
        """test list contest url."""
        url = reverse('contest:list')
        self.assertEqual(url, '/contest/')

    def test_url_vote_user(self):
        """test user's vote url."""
        url = reverse('contest:user_vote', args=[1234])
        self.assertEqual(url, '/contest/vote/1234')

    def test_url_depot_picture_user(self):
        """test the url for uploading a picture"""
        url = reverse('contest:add_picture_to_contest', args=[1234, 1234])
        self.assertEqual(url, '/contest/depot/1234/1234')