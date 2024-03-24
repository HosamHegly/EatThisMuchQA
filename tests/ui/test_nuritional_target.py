import time
import unittest
from infra.api.api_wrapper import APIWrapper
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.nutritional_target_page import NutritionalTargetPage
from logic.ui.planner_page import PlannerPage
from test_data.calorie_target import *
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
        self.test_name = self.id().split('.')[-1]
        self.target_id = None

    def tearDown(self):
        if self.target_id:
            try:
                self.nutritional_target.delete_nutritional_target(target_id=self.target_id)
            except Exception as e:
                print(f"Failed to delete nutritional target in tearDown: {e}")
        self.browser_wrapper.close_browser()

    def test_valid_nutritional_target_creation(self):
        try:
            response = self.nutritional_target.create_nutritional_target(body=valid_target[0]).json()
            self.target_id = response['data']['id']

            self.browser_wrapper.goto(urls['Nutritional_Target'])
            nutritional_targets_page = NutritionalTargetPage(self.driver)
            self.assertIn(response['data']['title'], nutritional_targets_page.get_target_titles(),
                          "Nutritional target wasn't added to the target page")
        except Exception as e:
            self.fail(f"Exception during test_valid_nutritional_target_creation: {e}")

    def test_invalid_nutritional_target_creation(self):
        try:
            response = self.nutritional_target.create_nutritional_target(body=invalid_target[0])
            if response.status_code != 400:
                self.fail("Invalid nutritional target creation should not succeed")
        except Exception as e:
            self.fail(f"Exception during test_invalid_nutritional_target_creation: {e}")

    def test_nutritional_target_change_setting(self):
        try:
            response = self.nutritional_target.create_nutritional_target(body=valid_target[1]).json()
            self.target_id = response['data']['id']

            self.meal_setting.change_nutritional_target(target_id=self.target_id)
            self.browser_wrapper.goto(urls['Planner_Page'])
            planner_page = PlannerPage(self.driver)
            planner_page.sync_page()
            target_cals = planner_page.get_target_cals()
            self.assertEqual(target_cals, valid_target[1]['calories'],
                             msg="Calorie target value didn't change in main page when changed in settings")
        except Exception as e:
            self.fail(f"Exception during test_nutritional_target_change_setting: {e}")