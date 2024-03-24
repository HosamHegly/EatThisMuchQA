import time
import unittest
import requests

from infra.api.api_wrapper import APIWrapper
from infra.ui.browser_wrapper import BrowserWrapper
from logic.api.food_addition_endpoint import FoodAdditionEndpoint
from logic.api.food_endpoint import FoodEndPoint
from logic.api.food_search_filter_endpoint import SearchFoodEndpoint
from logic.ui.food_search_popup import FoodSearchPopup
from logic.ui.planner_page import PlannerPage
from test_data.users import *
from test_data.urls import urls
from Utils.helper_functions import choose_random_number_in_range


class MealEditTest(unittest.TestCase):
    _non_parallel = True
    USER = get_valid_user('Hosam')

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.my_api = APIWrapper()
        self.search_filter_api = SearchFoodEndpoint(self.my_api)
        self.food_addition_api = FoodAdditionEndpoint(self.my_api)
        self.browser_wrapper.goto(urls['Planner_Page'])
        self.planner_page = PlannerPage(self.driver)
        self.food = FoodEndPoint(self.my_api)
        self.food_id = None

    def test_food_addition(self):
        try:
            before_cals = self.planner_page.get_total_calories()
            response = self.search_filter_api.search_by_cals(min_cals=300, max_cals=1000).json()
            food_api_list = response['data']['object_resource_uris']
            if not food_api_list:
                self.fail("No food items returned from the search")
            food_api = food_api_list[choose_random_number_in_range(0, len(food_api_list))]
            food_response = self.food.get_food_details(food_api).json()
            food_name = food_response['data']['food_name'].lower()
            food_cals = int(food_response['data']['calories'])
            food_addition_response = self.food_addition_api.add_food_to_breakfast(food_api=food_api).json()
            self.food_id = food_addition_response['data']['id']

            self.browser_wrapper.refresh()
            after_cal = self.planner_page.get_total_calories()

            self.assertIn(food_name, self.planner_page.get_breakfast_list(), "Food wasn't added to breakfast list")
            self.assertAlmostEqual(after_cal, before_cals + food_cals, delta=5,
                                   msg='Calorie count after food addition is incorrect')
        except Exception as e:
            self.fail(f"Exception during test_food_addition: {e}")

    def tearDown(self):
        if self.food_id:
            try:
                self.food_addition_api.remove_food_from_breakfast(self.food_id)
            except Exception as e:
                print(f"Failed to remove food from breakfast during cleanup: {e}")
        self.browser_wrapper.close_browser()
