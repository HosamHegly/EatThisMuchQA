from selenium.webdriver.common.by import By
from test_data.urls import urls
from infra.ui.base_page import BasePage
from logic.ui.create_nutritional_target_page import CreateNutritionalTargetPage


class MealSettings(BasePage):
    SELECT_TARGET = (By.XPATH, "//select[@id='nutrition_target_6']")
    SELECT_TARGET_OPTIONS = (By.XPATH, "//select[@id='nutrition_target_6']//option")

    def __init__(self, driver):
        super().__init__(driver)
        self.init_elements()

    def init_elements(self):
        self.select_button = self.wait_for_element_in_page_by_xpath(self.SELECT_TARGET[1])
        self.select_options = self._driver.find_elements(*self.SELECT_TARGET_OPTIONS)

    def change_target_setting(self, target_title):
        for option in self.select_options:
            if option.text == target_title:
                option.click()
