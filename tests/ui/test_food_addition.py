import time
import unittest

import requests
from parameterized import parameterized_class

from Utils.json_reader import get_config_data
from infra.api.api_wrapper import APIWrapper
from infra.jira_client import JiraClient
from infra.ui.browser_wrapper import BrowserWrapper
from logic.api.food_addition_endpoint import FoodAdditionEndpoint
from logic.api.food_endpoint import FoodEndPoint
from logic.api.food_search_filter_endpoint import SearchFoodEndpoint
from logic.ui.food_search_popup import FoodSearchPopup
from logic.ui.planner_page import PlannerPage
from test_data.users import *
from test_data.urls import urls
from Utils.helper_functions import choose_random_number_in_range


config = get_config_data()
browser_types = [(browser,) for browser in config["browser_types"]]


@parameterized_class(('browser',), browser_types)
class MealEditTest(unittest.TestCase):
    _non_parallel = True
    USER = get_valid_user('Hosam')
    browser = 'chrome'

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.browser)
        self.browser_wrapper.add_browser_cookie()
        self.my_api = APIWrapper()
        self.search_filter_api = SearchFoodEndpoint(self.my_api)
        self.food_addition_api = FoodAdditionEndpoint(self.my_api)
        self.browser_wrapper.goto(urls['Planner_Page'])
        self.planner_page = PlannerPage(self.driver)
        self.food = FoodEndPoint(self.my_api)
        self.jira_client = JiraClient()
        self.test_failed = False

    def test_food_addition_with_calorie_filter(self):
        """test food addition: send api for search by calorie filter, get an food api from reponse and add it breakfast with add food api call
        then check if food is added in breakfast with ui"""
        try:
            before_cals = self.planner_page.get_total_calories()
            response = self.search_filter_api.search_by_cals(min_cals=300, max_cals=1000).json()
            food_api_list = response['data']['object_resource_uris']
            food_api = food_api_list[choose_random_number_in_range(0, len(food_api_list))]
            food_response = self.food.get_food_details(food_api).json()
            food_name = food_response['data']['food_name'].lower()
            food_addition_response = self.food_addition_api.add_food_to_breakfast(food_api=food_api).json()
            self.food_id = food_addition_response['data']['id']
            self.browser_wrapper.refresh()
            self.assertIn(food_name, self.planner_page.get_breakfast_list(), "food wasn't added to breakfast list")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.browser_wrapper.close_browser()

        self.food_addition_api.remove_food_from_breakfast(self.food_id)
        self.test_name = self.id().split('.')[-1]
        if self.test_failed:
            summary = f"Test failed: {self.test_name}"
            description = f"{self.error_msg} browser {self.__class__.browser}"
            try:
                issue_key = self.jira_client.create_issue(summary=summary, description=description,
                                                          issue_type='Bug', project_key='NEW')
                print(f"Jira issue created: {issue_key}")
            except Exception as e:
                print(f"Failed to create Jira issue: {e}")
