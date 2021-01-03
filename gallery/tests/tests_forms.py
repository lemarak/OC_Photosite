"""Test the form for gallery (upload picture)."""


from django.test import SimpleTestCase

from gallery.forms import PictureForm


class PictureFormTests(SimpleTestCase):
    """ test picture's form """

    def test_picture_form_without_mandatory(self):
        """ test missing mandatory fields """
        form = PictureForm(data={
            "title": '',
            "file_name": '',
            "description": '',
            "camera": '',
            "lens": '',
            "place": '',
            "taken_date": '',
            "global_score": '',
            "upload_date": '',
            "categories": '',
            "user": ''
        })

        self.assertEqual(
            form.errors['title'][0], "Ce champ est obligatoire."
        )

    def test_picture_form_without_description(self):
        """ test missing description """
        form = PictureForm(data={
            "title": 'test',
            "file_name": 'test',
        })

        self.assertEqual(
            form.errors['description'][0], "Ce champ est obligatoire."
        )

    def test_picture_form_with_mandatory(self):
        """ test all mandatory's """
        form = PictureForm(data={
            "title": 'test',
            "file_name": 'test',
            "description": 'test',
        })

        self.assertTrue(form.is_valid)
