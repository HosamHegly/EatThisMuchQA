import unittest

import pytest
import HtmlTestRunner

from infra.api.api_wrapper import APIWrapper
from infra.jira_client import JiraClient
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.nutritional_target_page import NutritionalTargetPage
from logic.ui.planner_page import PlannerPage
from logic.api.nutritional_target_endpoint import NutritionalTargetEndPoint
from test_data.calorie_target import valid_target, invalid_target
from test_data.urls import urls
from logic.api.meal_settings_enpoint import MealSettingsEndPoint


class TestNutritionalTarget(unittest.TestCase):

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.my_api = APIWrapper()
        self.nutritional_target = NutritionalTargetEndPoint(self.my_api)
        self.meal_setting = MealSettingsEndPoint(self.my_api)
        self.jira_client = JiraClient()

        self.test_failed = False

    def test_valid_nutrional_target_creation(self):
        try:
            response = self.nutritional_target.create_nutritional_target(body=valid_target[0]).json()
            self.target_id = response['data']['id']

            self.browser_wrapper.goto(urls['Nutritional_Target'])
            self.nutritional_targets_page = NutritionalTargetPage(self.driver)
            self.assertIn(response['data']['title'], self.nutritional_targets_page.get_target_titles(),
                          "nutritional target wasn't added to the target page")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_invalid_nutrional_target_creation(self):
        try:
            response = self.nutritional_target.create_nutritional_target(body=invalid_target[0]).json()
            self.target_id = response['data']['id']

            self.browser_wrapper.goto(urls['Nutritional_Target'])
            self.nutritional_targets_page = NutritionalTargetPage(self.driver)
            self.assertNotIn(response['data']['title'], self.nutritional_targets_page.get_target_titles(),
                             "invalid nutritional target was added to the target page")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_nutrional_target_change_setting(self):
        try:
            response = self.nutritional_target.create_nutritional_target(body=valid_target[1]).json()
            self.target_id = response['data']['id']
            self.meal_setting.change_nutritional_target(target_id=self.target_id)
            self.browser_wrapper.goto(urls['Planner_Page'])
            self.planner_page = PlannerPage(self.driver)
            self.planner_page.sync_page()
            target_cals = self.planner_page.get_target_cals()
            self.nutritional_target.delete_nutritional_target(target_id=self.target_id)
            self.assertEqual(target_cals, valid_target[1]['calories'],
                             msg="calorie target value didn't change in main page when changed in settings")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.browser_wrapper.close_browser()

        self.nutritional_target.delete_nutritional_target(target_id=self.target_id)

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
