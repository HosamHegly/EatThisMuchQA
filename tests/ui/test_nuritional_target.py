import time
import unittest

from parameterized import parameterized_class

from Utils.json_reader import get_config_data
from infra.api.api_wrapper import APIWrapper
from infra.jira_client import JiraClient
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.nutritional_target_page import NutritionalTargetPage
from logic.ui.planner_page import PlannerPage
from logic.api.nutritional_target_endpoint import NutritionalTargetEndPoint
from test_data.calorie_target import valid_target, invalid_target
from test_data.urls import urls
from logic.api.meal_settings_enpoint import MealSettingsEndPoint
from Utils.helper_functions import choose_random_number_in_range,generate_random_5_letter_name
config = get_config_data()
browser_types = [(browser,) for browser in config["browser_types"]]


class TestNutritionalTarget(unittest.TestCase):
    browser = 'chrome'

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.browser)
        self.browser_wrapper.add_browser_cookie()
        self.my_api = APIWrapper()
        self.nutritional_target_endpoint = NutritionalTargetEndPoint(self.my_api)
        self.browser_wrapper.goto(urls['Nutritional_Target'])
        self.nutritional_targets_page = NutritionalTargetPage(self.driver)
        self.meal_setting = MealSettingsEndPoint(self.my_api)
        self.jira_client = JiraClient()
        self.test_failed = False

    def test_valid_nutrional_target_creation(self):
        """send api call to create valid target with random name and calorie count then check if it's in the page
        with ui"""
        try:
            body = valid_target[0]
            body['title'] = generate_random_5_letter_name()
            body['calories'] = choose_random_number_in_range(3000,3500)
            response = self.nutritional_target_endpoint.create_nutritional_target(body=body).json()
            self.target_id = response['data']['id']
            self.browser_wrapper.refresh()
            self.assertIn(response['data']['title'], self.nutritional_targets_page.get_target_titles(),
                          "nutritional target wasn't added to the target page")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_invalid_nutrional_target_creation(self):
        """negative test: send api call
         to create valid target with random name and calorie count then check if it's in the page with ui"""

        try:
            body = invalid_target[0]
            body['title'] = generate_random_5_letter_name()
            body['calories'] = choose_random_number_in_range(100000000, 1000000000)
            response = self.nutritional_target_endpoint.create_nutritional_target(body=body).json()
            self.target_id = response['data']['id']
            self.browser_wrapper.refresh()
            time.sleep(2)
            self.assertNotIn(response['data']['title'], self.nutritional_targets_page.get_target_titles(),
                             "invalid nutritional target was added to the target page")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.browser_wrapper.close_browser()

        self.nutritional_target_endpoint.delete_nutritional_target(target_id=self.target_id)

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
