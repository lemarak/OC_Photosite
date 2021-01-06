"""functional tests using selenium and LiveServerTestCase."""
from datetime import datetime, date
import time

from django.test import LiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager  # easy to install

from gallery.models import Picture


class ReviewFunctionalTest(LiveServerTestCase):
    """ functionnal tests on review """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.options = Options()
        # cls.options.add_argument("--headless")
        cls.browser = Chrome(ChromeDriverManager().install(),
                             options=cls.options)
        cls.browser.implicitly_wait(3)

        # create user
        cls.user = get_user_model().objects.create(
            username='test_login',
            email='test@example.com'
        )
        cls.user.set_password('123test')
        cls.user.save()

        # create picture
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.picture = Picture(
            title='test_title',
            file_name=SimpleUploadedFile(
                name='small.gif', content=small_gif, content_type='image/gif'),
            description='test_description',
            technical='test_technical',
            camera='test_camera',
            place='test_place',
            taken_date=date(2021, 1, 1),
            user=cls.user,
            upload_date=datetime.now(),
        )
        cls.picture.save()
        

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def login_user(self, username, pwd):
        """method simulating the connection of a user."""
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/accounts/login/'))
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submission_button = self.browser.find_element_by_class_name(
            'btn-success')

        username_input.send_keys(username)
        password_input.send_keys(pwd)
        submission_button.click()

    def add_review(self):
        """ method for upload a picture """
        url = "/review/create/%s" % self.picture.id
        self.browser.get("%s%s" %
                         (str(self.live_server_url), url))

        select = Select(self.browser.find_element_by_id(
            "id_score_intention"))
        select.select_by_index(4)
        select = Select(self.browser.find_element_by_id(
            "id_score_technical"))
        select.select_by_index(4)
        select = Select(self.browser.find_element_by_id(
            "id_score_picture"))
        select.select_by_index(4)
        select = Select(self.browser.find_element_by_id(
            "id_score_global"))
        select.select_by_index(4)

        self.browser.find_element_by_id(
            "id_comment_intention").send_keys("Commentaire intention")

        submission_button = self.browser.find_element_by_class_name(
            'btn-secondary')
        submission_button.click()
        time.sleep(2)
        html = self.browser.page_source
        self.assertInHTML("""
                    <h4 class="rouge-fonce">Critique de test_login</h4>
                        """,
                          html)
        self.assertInHTML("""
           <strong>Note moyenne de la revue : 4,0</strong>
                """,
                          html)

    def test_add_review_and_display(self):
        """ identification, add review and display review """
        # identification
        self.login_user('test_login', '123test')

        # add review
        self.add_review()

        # see review
        self.browser.implicitly_wait(3)
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/review/list'))
        time.sleep(0.5)
        link = self.browser.find_element_by_partial_link_text('Voir la critique')
        link.click()
        html = self.browser.page_source
        self.assertInHTML("""
                    <h4 class="rouge-fonce">Critique de test_login</h4>
                        """,
                          html)
        self.browser.quit()