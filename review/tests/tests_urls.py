"""test the urls."""
from django.test import SimpleTestCase
from django.urls import reverse


class ReviewUrlTests(SimpleTestCase):

    def test_url_one_review(self):
        """test the review picture url."""
        url = reverse('review:detail', args=[1234])
        self.assertEqual(url, '/review/detail/1234')

    def test_url_create_review_form(self):
        """test the create review form url."""
        url = reverse('review:review_create', args=[1234])
        self.assertEqual(url, '/review/create/1234')

    # def test_url_update_review_form(self):
    #     """test the update review form url."""
    #     url = reverse('review_update', args=[1234])
    #     self.assertEqual(url, '/review/update/1234')

    # def test_url_delete_review(self):
    #     """test the update review form url."""
    #     url = reverse('review_delete', args=[1234])
    #     self.assertEqual(url, '/review/delete/1234')
    