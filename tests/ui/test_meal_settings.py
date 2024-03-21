import time
import unittest
from infra.api.api_wrapper import APIWrapper
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.planner_page import PlannerPage
from test_data.calorie_target import *
from logic.api.nutritional_target_endpoint import NutritionalTargetEndPoint
from test_data.calorie_target import valid_target
from test_data.urls import urls
from logic.api.meal_settings_enpoint import MealSettingsEndPoint


class TestMealSetting(unittest.TestCase):
    INVALID_TARGETS = invalid_target

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.my_api = APIWrapper()
        self.nutritional_target = NutritionalTargetEndPoint(self.my_api)
        self.meal_setting = MealSettingsEndPoint(self.my_api)
        self.test_name = self.id().split('.')[-1]

    def test_nutrional_target_change_setting(self):
        response = self.nutritional_target.create_nutritional_target(body=valid_target)
        target_id=response['data']['id']
        self.meal_setting.change_nutritional_target(target_id=target_id)
        self.browser_wrapper.goto(urls['Planner_Page'])
        self.planner_page = PlannerPage(self.driver)
        self.planner_page.sync_page()
        target_cals = self.planner_page.get_target_cals()
        self.nutritional_target.delete_nutritional_target(target_id=target_id)
        self.assertEqual(target_cals,valid_target['calories'])

    def tearDown(self):
        self.browser_wrapper.close_browser()
