"""Test the form for review."""


from django.test import SimpleTestCase

from review.forms import ReviewForm


class CreateReviewFormTests(SimpleTestCase):
    """ test create review's form """

    def test_review_forms_not_all_score(self):
        """ test missing score """
        form = ReviewForm(data={
            "score_intention": 4,
            "score_technical": 4,
            "score_picture": 4,
            "comment_intention": "comment_intention",
            "comment_technical": "comment_technical",
            "comment_picture": "comment_picture",
            "comment_global": "comment_global"
        })

        self.assertEqual(
            form.errors['score_global'][0], "Ce champ est obligatoire."
        )

    def test_review_forms_all_score(self):
        """ test all score is valid """
        form = ReviewForm(data={
            "score_intention": 4,
            "score_technical": 4,
            "score_picture": 4,
            "score_global": 4,
            "comment_intention": "comment_intention",
            "comment_technical": "comment_technical",
            "comment_picture": "comment_picture",
            "comment_global": "comment_global"
        })

        self.assertTrue(form.is_valid)

    def test_review_forms_without_comment(self):
        """ test is valid without comment """
        form = ReviewForm(data={
            "score_intention": 4,
            "score_technical": 4,
            "score_picture": 4,
            "score_global": 4
        })

        self.assertTrue(form.is_valid)
