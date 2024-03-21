from selenium.common import TimeoutException
import unittest

from test_data import users
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.login_page import LoginPage


class LoginPageTest(unittest.TestCase):
    VALID_USERS = users.valid_users
    INVALID_USERS = users.invalid_users

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.login_page = LoginPage(self.driver)

    def test_login_with_valid_user(self):
        for user in self.VALID_USERS:
            self.login_page.login_with_email_password(user['email'], user['password'])
            self.assertTrue(self.login_page.is_main_page_title())

    def test_login_with_valid_user(self):
        for user in self.INVALID_USERS:
            self.login_page.login_with_email_password(user['email'], user['password'])
            try:
                self.login_page.wait_for_error_message()
                self.assertIn('enter a correct username and password', self.login_page.get_page_text())
                self.login_page.clear_input_fields()

            except TimeoutException:
                self.fail("Error message was not found within the given time")

    def tearDown(self):
        self.browser_wrapper.close_browser()
