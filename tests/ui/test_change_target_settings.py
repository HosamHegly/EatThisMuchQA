import unittest
import time

import pytest
from parameterized import parameterized_class
from Utils.json_reader import get_config_data
from infra.api.api_wrapper import APIWrapper
from infra.jira_client import JiraClient
from infra.ui.browser_wrapper import BrowserWrapper
from logic.api.meal_settings_enpoint import MealSettingsEndPoint
from logic.api.nutritional_target_endpoint import NutritionalTargetEndPoint
from logic.ui.meal_settings import MealSettings
from logic.ui.menu import Menu
from logic.ui.planner_page import PlannerPage
from logic.ui.nutritional_target_page import NutritionalTargetPage
from Utils.helper_functions import generate_random_5_letter_name, choose_random_number_in_range
from test_data.calorie_target import valid_target
from test_data.urls import urls

config = get_config_data()
browser_types = [(browser,) for browser in config["browser_types"]]


@pytest.mark.serial
@parameterized_class(('browser',), browser_types)
class TestNutritionalTargetSetting(unittest.TestCase):
    browser = 'chrome'
    _non_parallel = True

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.my_api = APIWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.browser)
        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Planner_Page'])
        self.planner_page = PlannerPage(self.driver)
        self.jira_client = JiraClient()
        self.test_failed = False

    def test_create_target_and_change_meal_settings_to_target(self):
        """'end to end ui test that creates a natrutional target then changes to the meal setting to that target then goes
        to planner page and check's target calorie"""
        try:
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
                                                            min_proteins=85, max_proteins=309, min_fats=52,
                                                            max_fats=138, fiber=35)
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
            time.sleep(2)

            self.menu.go_to_nutritional_target_page()
            time.sleep(1)
            self.nutritional_target.delete_last_target()
            time.sleep(2)
            self.assertEqual(calories, target_cals,
                             "target calories didn't match the target we chose in settings")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_nutrional_target_change_setting(self):
        """'send an api call that creates a target then an api that changes settings than with ui
        go to planner page, sync page then check target calories"""
        try:

            self.nutritional_target_api = NutritionalTargetEndPoint(self.my_api)
            self.meal_setting_api = MealSettingsEndPoint(self.my_api)
            response = self.nutritional_target_api.create_nutritional_target(body=valid_target[1]).json()
            self.target_id = response['data']['id']
            self.meal_setting_api.change_nutritional_target(target_id=self.target_id)
            self.browser_wrapper.refresh()
            self.planner_page.sync_page()
            target_cals = self.planner_page.get_target_cals()
            self.nutritional_target_api.delete_nutritional_target(target_id=self.target_id)
            self.assertEqual(target_cals, valid_target[1]['calories'],
                             msg="calorie target value didn't change in main page when changed in settings")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.browser_wrapper.close_browser()

        self.test_name = self.id().split('.')[-1]
        if self.test_failed:
            summary = f"Test failed: {self.test_name}"
            description = f"{self.error_msg} browser {self.__class__.browser}"
            try:
                issue_key = self.jira_client.create_issue(summary=summary, description=description, issue_type='Bug',
                                                          project_key='NEW')
                print(f"Jira issue created: {issue_key}")
            except Exception as e:
                print(f"Failed to create Jira issue: {e}")
