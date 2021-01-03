"""test the urls."""
from django.test import SimpleTestCase
from django.urls import reverse


class GalleryUrlTests(SimpleTestCase):
    """  tests urls from app gallery """

    def test_url_home(self):
        """ test home url """
        url = reverse('gallery:home')
        self.assertEqual(url, '/')

    def test_url_gallery_with_one_parameter(self):
        """test the gallery url."""
        url = reverse('gallery:pictures_list', args=['action'])
        self.assertEqual(url, '/pictures/action')

    def test_url_gallery_with_two_parametes(self):
        """test the gallery url."""
        url = reverse('gallery:pictures_list', args=['action', 1234])
        self.assertEqual(url, '/pictures/action/1234')

    def test_url_picture_display(self):
        """test picture display url """
        url = reverse('gallery:picture_detail', args=['1234'])
        self.assertEqual(url, '/picture/1234')

    def test_url_categories_list(self):
        """test categories url """
        url = reverse('gallery:categories')
        self.assertEqual(url, '/categories')

    def test_url_images_upload_form(self):
        """test image upload form url """
        url = reverse('gallery:image_upload')
        self.assertEqual(url, '/image-upload')
