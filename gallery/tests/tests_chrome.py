"""functional tests using selenium and LiveServerTestCase."""
import time
import os

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager  # easy to install

from gallery.models import Category


class GalleryFunctionalTest(LiveServerTestCase):
    """ functionnal tests on gallery """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.options = Options()
        # cls.options.add_argument("--headless")
        cls.browser = Chrome(ChromeDriverManager().install(),
                             options=cls.options)
        cls.browser.implicitly_wait(3)

        User = get_user_model()
        cls.user = User.objects.create_user(
            username='test_login',
            email='test_login@example.com',
            password='123test'
        )

        # create category
        for indice in range(1, 6):
            category = Category(
                name="category_test_%s" % indice,
                in_menu=True,
                order_menu=1
            )
            category.save()

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

    def add_picture(self):
        """ method for upload a picture """
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/image-upload'))

        self.browser.find_element_by_id(
            "id_title").send_keys("Titre photo")
        self.browser.find_element_by_id(
            "id_file_name").send_keys(os.getcwd()+"/gallery/tests/test.png")
        self.browser.find_element_by_id(
            "id_description").send_keys("Description photo")
        self.browser.find_element_by_id(
            "id_technical").send_keys("Technique photo")
        select = Select(self.browser.find_element_by_id(
            "id_categories"))
        select.select_by_index(1)

        submission_button = self.browser.find_element_by_class_name(
            'btn-success')
        submission_button.click()
        # time.sleep(2)
        html = self.browser.page_source
        self.assertInHTML("""
                    <h4 class=" rouge-fonce">Titre photo, postée par <a href="/pictures/user/%s">
                            test_login</a> le 06/01/2021
                    </h4>
                        """ % self.user.id,
                          html)

    def test_add_picture_and_display(self):
        """ identification, upload and View photo from gallery """
        # identification
        self.login_user('test_login', '123test')
        time.sleep(0.5)
        # upload picture
        self.add_picture()
        time.sleep(0.5)

        # see picture
        self.browser.implicitly_wait(3)
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/pictures/last'))
        time.sleep(0.5)
        link = self.browser.find_element_by_partial_link_text('voir')
        link.click()
        html = self.browser.page_source
        self.assertInHTML("""
                    <h4 class=" rouge-fonce">Titre photo, postée par <a href="/pictures/user/%s">
                            test_login</a> le 06/01/2021
                    </h4>
                        """ % self.user.id,
                          html)
        self.browser.quit()
