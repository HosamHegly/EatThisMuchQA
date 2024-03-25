import time

import unittest

from infra.api.api_wrapper import APIWrapper
from infra.jira_client import JiraClient
from infra.ui.browser_wrapper import BrowserWrapper
from logic.api.meal_settings_enpoint import MealSettingsEndPoint
from test_data.calorie_target import *
from test_data.users import *
from logic.ui.weight_goal_page import WeightGoalPage
from test_data.urls import urls


class WeightGoalTest(unittest.TestCase):


    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Weight_Goal'])
        self.my_api = APIWrapper()
        self.weight_goals_page = WeightGoalPage(self.driver)
        self.jira_client = JiraClient()
        self.test_failed = False

    def test_invalid_weight_input_negative(self):
        try:
            self.weight_goals_page.update_weight(-1)
            self.assertTrue(
                self.weight_goals_page.get_validation_message() in ['Value must be greater than or equal to 0.',
                                                                    'Please select a value that is no less than 0.'])
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_invalid_weight_input_greater_than_upper_limit(self):
        try:
            self.weight_goals_page.update_weight(1000)
            self.assertTrue(
                self.weight_goals_page.get_validation_message() in ['Value must be less than or equal to 999.',
                                                                    'Please select a value that is no more than 999.'])
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_valid_weight_input(self):
        try:
            weight = 80
            self.mealsettings = MealSettingsEndPoint(self.my_api)
            self.mealsettings.change_weight(80)
            self.weight_goals_page.update_weight(weight)
            self.assertIn(str(weight), self.weight_goals_page.get_last_updated_label())
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.browser_wrapper.close_browser()

        self.test_name = self.id().split('.')[-1]
        if self.test_failed:
            summary = f"Test failed: {self.test_name} "
            description = f"{self.error_msg} browser {self.__class__.browser}"
            try:
                issue_key = self.jira_client.create_issue(summary=summary, description=description,
                                                          issue_type='Bug', project_key='NEW')
                print(f"Jira issue created: {issue_key}")
            except Exception as e:
                print(f"Failed to create Jira issue: {e}")
