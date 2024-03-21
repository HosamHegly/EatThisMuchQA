from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from infra.ui.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_FIELD = (By.XPATH, "//input[@id='username']")
    PASSWORD_FIELD = (By.XPATH, "//input[@autocomplete='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = "//div[@class='warning svelte-1vdzk1k']"

    def __init__(self, driver):
        super().__init__(driver)
        self.init_elements()

    def init_elements(self):
        self.email_field = self._driver.find_element(*self.EMAIL_FIELD)
        self.password_field = self._driver.find_element(*self.PASSWORD_FIELD)
        self.login_button = self._driver.find_element(*self.LOGIN_BUTTON)

    def fill_email_field(self, email):
        self.email_field.send_keys(email)

    def fill_password_field(self, password):
        self.password_field.send_keys(password)

    def login_with_email_password(self, email, password):
        self.fill_email_field(email)
        self.fill_password_field(password)
        self.login_button.click()

    def clear_input_fields(self):
        self.email_field.clear()
        self.password_field.clear()

    def is_main_page_title(self):
        return WebDriverWait(self._driver, 10).until(EC.title_contains('Today'))

    def wait_for_error_message(self):
        self.wait_for_element_in_page_by_xpath(self.ERROR_MESSAGE)
