"""functional tests using selenium and TestCase."""
import time

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager  # easy to install


class SignUpTest(LiveServerTestCase):
    """Functionnal tests for signup page."""

    def setUp(self):
        """Method called to prepare the test fixture."""
        self.options = Options()
        self.options.add_argument("--headless")
        self.browser = Chrome(ChromeDriverManager().install(),
                              options=self.options)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        """Method called immediately after the test method has been called and
        the result recorded."""
        self.browser.quit()

    def signup_form(self, action):
        """method simulating the signup of a user.

        param: action_id (button or key)
        """
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/accounts/signup/'))
        email_input = self.browser.find_element_by_id('id_email')
        username_input = self.browser.find_element_by_id('id_username')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        submission_button = self.browser.find_element_by_class_name(
            'btn-success')

        username_input.send_keys('test_username_selenium')
        email_input.send_keys('test_email_selenium@example.com')
        password1_input.send_keys('test_1234')
        password2_input.send_keys('test_1234')
        if (action == "button"):
            submission_button.click()
        else:
            password2_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
        redirection_url = str(self.live_server_url) + "/accounts/login/"
        current_url = self.browser.current_url
        self.assertEqual(redirection_url,
                         current_url)

    def test_signup_with_button(self):
        """test signup with click on button."""
        self.signup_form('button')

    def test_signup_with_key(self):
        """test signup with enter."""
        self.signup_form('key')


class SignInFormTest(LiveServerTestCase):
    """Functionnal tests for signin page."""

    def setUp(self):
        """Method called to prepare the test fixture."""
        self.options = Options()
        self.options.add_argument("--headless")
        self.browser = Chrome(ChromeDriverManager().install(),
                              options=self.options)
        self.browser.implicitly_wait(3)
        User = get_user_model()
        User.objects.create_user(
            username='test_login',
            email='test_login@example.com',
            password='123test'
        )

    def tearDown(self):
        """Method called immediately after the test method has been called and
        the result recorded."""
        self.browser.quit()

    def signin_form(self, action):
        """method simulating the signin of a user.

        param: action_id (button or key)
        """
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/accounts/login/'))
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')

        username_input.send_keys('test_login')
        password_input.send_keys('123test')
        if (action == "button"):
            submission_button = self.browser.find_element_by_class_name(
                'btn-success')
            submission_button.click()
        else:
            password_input.send_keys(Keys.ENTER)

        time.sleep(0.5)
        redirection_url = str(self.live_server_url) + '/'
        current_url = self.browser.current_url
        html = self.browser.page_source
        self.assertEqual(redirection_url,
                         current_url)
        self.assertInHTML("""
                    <h2>Bienvenue <strong>test_login</strong>  sur PhotoSite ! Ici vous pouvez...
      </h2>
                        """,
                          html)

    def test_signin_with_button(self):
        """test signup with click on button."""
        self.signin_form('button')

    def test_signin_with_key(self):
        """test signup with key enter."""
        self.signin_form('key')

    def test_bad_signin(self):
        """test signin with bad mail."""
        url_login = "%s%s" % (str(self.live_server_url), '/accounts/login/')
        self.browser.get(url_login)
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submission_button = self.browser.find_element_by_class_name(
            'btn-success')

        username_input.send_keys('test_login_ba')
        password_input.send_keys('123test')
        submission_button.click()

        time.sleep(0.5)
        html = self.browser.page_source
        self.assertEqual(url_login,
                         self.browser.current_url)
        self.assertInHTML("<h2>Connexion</h2>", html)
