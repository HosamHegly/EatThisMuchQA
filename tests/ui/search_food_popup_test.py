import unittest

from Utils.helper_functions import is_contained_in
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.food_search_popup import FoodSearchPopup
from logic.ui.planner_page import PlannerPage
from test_data import food, users
from test_data.urls import urls


class FoodSearchPopupTest(unittest.TestCase):
    USER = users.get_valid_user('Hosam')
    VALID_FOOD = food.valid_search_food_names
    INVALID_FOOD = food.invalid_search_food_names



    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)

        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Planner_Page'])
        self.planner_page = PlannerPage(self.driver)
        self.planner_page.click_add_food_to_meal_button('Breakfast')

    def test_search_food_with_valid_food_name(self):
        self.food_search_popup = FoodSearchPopup(self.driver)
        for food_name in self.VALID_FOOD:
            self.food_search_popup.fill_search_field(food_name)

            all_food_results = self.food_search_popup.get_all_results_food_names_and_ingredients()
            for food in all_food_results:
                self.assertTrue(food_name in food['name'] or is_contained_in(food_name, food['ingredient']))
            self.food_search_popup.clear_search_field()

    def test_calorie_filter_feature(self):
        self.food_search_popup = FoodSearchPopup(self.driver)
        min_calories = 500
        max_calories = 1000
        self.food_search_popup.fill_min_calories_filter(min_calories)
        self.food_search_popup.fill_max_calories_filter(max_calories)
        for calories in self.food_search_popup.get_all_search_results_calories():
            self.assertGreaterEqual(calories, min_calories,
                                    "Food result calories is less than the minumum calories input in the filter")
            self.assertLessEqual(calories, max_calories,
                                 "Food result calories is greater than the max calories input in the filter")

    '''def test_search_food_with_invalid_food_name(self):
        self.food_search_popup = FoodSearchPopup(self.driver)
        for invalid_food_name in self.INVALID_FOOD:
            self.food_search_popup.fill_search_field(invalid_food_name)
            self.assertTrue(self.food_search_popup.is_results_empty())
            self.food_search_popup.clear_search_field()'''

    def tearDown(self):

        self.browser_wrapper.close_browser()
