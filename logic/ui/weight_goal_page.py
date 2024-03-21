import time
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_data.urls import urls
from infra.ui.base_page import BasePage


class WeightGoalPage(BasePage):
    WEIGHT_INPUT = (By.XPATH, "//input[@name='todays_weight']")
    UPDATE_BUTTON = (By.XPATH, "//button[@type='submit']")
    LAST_UPDATED_LABEL = (By.XPATH, "//p[@class='last-update svelte-1sa5wwx']")

    def __init__(self, driver):
        super().__init__(driver)
        self._driver.get(urls['Weight_Goal'])
        self.init_elements()

    def init_elements(self):
        self.weight_input = WebDriverWait(self._driver, 20).until(EC.presence_of_element_located(self.WEIGHT_INPUT))
        self.update_button = self._driver.find_element(*self.UPDATE_BUTTON)

    def init_last_update(self):
        time.sleep(2)
        self.last_updated = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(self.LAST_UPDATED_LABEL))

    def get_last_updated_label(self):
        self.init_last_update()
        return self.last_updated.text

    def update_weight(self, weight):
        WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.WEIGHT_INPUT)).send_keys(weight)
        self.update_button.click()

    def clear_weight_input(self):
        self.weight_input.clear()

    def get_validation_message(self):
        return self._driver.execute_script("return arguments[0].validationMessage", self.weight_input)
