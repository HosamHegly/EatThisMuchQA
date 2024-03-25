import time
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import *

from infra.ui.base_page import BasePage


class PlannerPage(BasePage):
    EDIT_DAY_BUTTON = (By.XPATH, "//button[./span[contains(text(),'Edit')]]")
    GENERATE_BUTTON = (By.XPATH, "//button[./span[contains(text(),'Generate')]]")
    MEALS_TITLE = (By.XPATH, "//h2[contains(text(),'Meals')]")
    CALORIES = (By.XPATH, "//*[@id='app-content']/div/div/div/div/section/section[1]/div/table/tbody[1]/tr[1]/td[1]")
    REGENERATE = (By.XPATH, "//button[@title='Regenerate Day']")
    REGENERATE_POPUP_BUTTON = (By.XPATH, "//button[@class='_interaction_11et8_1 primary svelte-1m78l37']")
    BREAKFAST_LIST = (
        By.XPATH,
        "//section[./header[./h3[text()='Breakfast']]]//span[@class='food-name _class_1x8vs_1 svelte-ncaeor']")
    TARGET_CALORIE = (By.XPATH, "//*[@id='app-content']/div/div/div/div/section/section[1]/div/table/tbody[1]/tr["
                                "1]/td[2]")
    SYNC_BUTTON = (By.XPATH, "//*[@id='app-content']/div/div/div/div/section/div/div[1]/div[2]/div/button")
    MENU_BUTTON = (By.XPATH, "//button[@title='Open Menu']")

    def __init__(self, driver):
        super().__init__(driver)
        self.init_elements()

    def init_elements(self):
        self.init_edit_day_button()
        self.regen_button = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located(self.REGENERATE))
        self.menu_button = self._driver.find_element(*self.MENU_BUTTON)

    def init_calories(self):
        self.target_calorie = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located(self.TARGET_CALORIE)).text
        self.calories = self._driver.find_element(*self.CALORIES).text

    def sync_page(self):
        if len(self._driver.find_elements(*self.SYNC_BUTTON))> 0:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.SYNC_BUTTON)).click()
            time.sleep(2)

    def init_edit_day_button(self):
        self.wait_for_element_in_page_by_xpath(self.EDIT_DAY_BUTTON[1])
        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.EDIT_DAY_BUTTON))
        except:
            ElementNotInteractableException("can't click on ''Edit Day")
        self.edit_day = self._driver.find_element(*self.EDIT_DAY_BUTTON)

    def add_food_button_by_meal_locator(self, meal):
        return f"//section[./header[./h3[contains(text(),'{meal}')]]]//button[./span[contains(text(),'Add Food')]]"

    def init_add_food_button(self, meal):
        formated_string_locator = self.add_food_button_by_meal_locator(meal)
        if meal not in ('Breakfast', 'Dinner', 'Lunch', 'Snack'):
            raise ValueError("invalid meal name input should be 'breakfast','dinner','lunch' or 'snack'")

        self.add_food_button = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, formated_string_locator)))

    def is_edit_day_button_active(self):
        return 'active' in self.edit_day.get_attribute("class")

    def click_add_food_to_meal_button(self, meal):
        self.init_edit_day_button()
        if not self.is_edit_day_button_active():
            self.edit_day.click()

        self.init_add_food_button(meal)
        self.add_food_button.click()

    def get_total_calories(self):
        time.sleep(1)
        self.init_calories()
        return int(self.calories)

    def is_meal_generated(self):
        if len(self._driver.find_elements(*self.GENERATE_BUTTON)) > 0:
            return False
        return True

    def regenerate_meal_plan(self):
        time.sleep(2)
        self.regen_button = WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.REGENERATE))
        self.regen_button.click()
        WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(self.REGENERATE_POPUP_BUTTON)).click()

    def init_breakfast_list(self):
        self.breakfast_list = self.wait_for_element_in_page_by_xpath(self.BREAKFAST_LIST[1])
        self.breakfast_list = self._driver.find_elements(*self.BREAKFAST_LIST)

    def get_breakfast_list(self):
        food_list = []
        self.init_breakfast_list()
        for food in self.breakfast_list:
            food_list.append(food.text.lower())
        return food_list

    def get_target_cals(self):
        self.init_calories()
        return int(self.target_calorie)

    def go_to_menu(self):
        self.menu_button.click()
