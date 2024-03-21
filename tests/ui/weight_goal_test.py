import time

import unittest

from infra.ui.browser_wrapper import BrowserWrapper
from test_data.calorie_target import *
from test_data.users import *
from logic.ui.weight_goal_page import WeightGoalPage
from test_data.urls import urls


class WeightGoalTest(unittest.TestCase):
    VALID_TARGETS = valid_targets
    INVALID_TARGETS = invalid_target
    USER = get_valid_user('Hosam')

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Weight_Goal'])
        time.sleep(2)

        self.weight_goals_page = WeightGoalPage(self.driver)

    def test_invalid_weight_input_negative(self):
        self.weight_goals_page.update_weight(-1)
        self.assertTrue(self.weight_goals_page.get_validation_message() in['Value must be greater than or equal to 0.','Please select a value that is no less than 0.'])

    def test_invalid_weight_input_greater_than_upper_limit(self):
        self.weight_goals_page.update_weight(1000)
        self.assertTrue(self.weight_goals_page.get_validation_message() in['Value must be less than or equal to 999.','Please select a value that is no more than 999.'])

    def test_valid_weight_input(self):
        weight = 80
        self.weight_goals_page.update_weight(weight)
        self.assertIn(str(weight),self.weight_goals_page.get_last_updated_label())
        weight= 100
        self.weight_goals_page.update_weight(weight)
        self.assertIn(str(weight),self.weight_goals_page.get_last_updated_label())



    def tearDown(self):
        self.browser_wrapper.close_browser()
