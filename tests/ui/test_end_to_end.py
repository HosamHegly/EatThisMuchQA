import unittest
import time

from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.meal_settings import MealSettings
from logic.ui.menu import Menu
from logic.ui.planner_page import PlannerPage
from logic.ui.nutritional_target_page import NutritionalTargetPage
from Utils.helper_functions import generate_random_5_letter_name, choose_random_number_in_range
from test_data.urls import urls


class NutritionalTargetEndToEndTest(unittest.TestCase):

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Planner_Page'])
        self.planner_page = PlannerPage(self.driver)

    def test_create_target_and_change_meal_settings_to_target(self):
        self.planner_page.go_to_menu()
        self.menu = Menu(self.driver)
        time.sleep(1)
        self.menu.go_to_diet_and_nutrition()
        time.sleep(1)
        self.menu.go_to_nutritional_target_page()
        time.sleep(1)
        self.nutritional_target = NutritionalTargetPage(self.driver)
        title = generate_random_5_letter_name()
        calories = choose_random_number_in_range(3000, 3500)
        self.nutritional_target.create_nurtional_target(title, calories=calories, min_carbs=176, max_carbs=309,
                                                        min_proteins=85, max_proteins=309, min_fats=52, max_fats=138,fiber=35)
        time.sleep(1)
        self.menu.go_to_meal_and_schedule()
        time.sleep(1)
        self.menu.go_to_meal_settings()
        time.sleep(1)
        self.meal_settings = MealSettings(self.driver)
        self.meal_settings.change_target_setting(title)
        time.sleep(2)
        self.menu.go_to_planner_page()
        target_cals = self.planner_page.get_target_cals()
        time.sleep(4)

        self.menu.go_to_nutritional_target_page()
        time.sleep(1)
        self.nutritional_target.delete_last_target()
        time.sleep(2)
        self.assertEqual(calories, target_cals,
                         "target calories didn't match the target we chose in settings")

    def tearDown(self):
        self.browser_wrapper.close_browser()