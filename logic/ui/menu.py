from selenium.webdriver.common.by import By

from infra.ui.base_page import BasePage


class Menu(BasePage):
    NUTRITIONAL_TARGET_NAVIGATION = (By.XPATH, "//a[@type='button']/span[text()='Nutrition Targets']")
    MENU = (By.XPATH, "//button[@title='Open Menu']")
    DIET_NUTRITION_NAVIGATION = (By.XPATH, "//button[text() = 'Diet & Nutrition']")

    def __init__(self, driver):
        self._driver = driver
        self.init_menue()

    def init_menue(self):
        self.menu = self.wait_for_element_in_page_by_xpath(self.MENU[1])

    def click_menu(self):
        self.menu.click()
    def click_diet_and_nutrition(self):
        self.wait_for_element_in_page_by_xpath(self.DIET_NUTRITION_NAVIGATION[1]).click()


    def go_to_nutritional_target_page(self):
        self.wait_for_element_in_page_by_xpath(self.NUTRITIONAL_TARGET_NAVIGATION[1]).click()
