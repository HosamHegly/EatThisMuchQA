import unittest
from Utils.helper_functions import calculate_macro_calories
from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.create_nutritional_target_page import CreateNutritionalTargetPage
from logic.ui.nutritional_target_page import NutritionalTargetPage
from test_data.calorie_target import *
from test_data.urls import urls


class NutritionalTargetsValuesTest(unittest.TestCase):
    VALID_TARGETS = valid_targets
    INVALID_TARGETS = invalid_target
    USER = valid_targets[0]

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)
        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Nutritional_Target'])
        self.nutritional_targets_page = NutritionalTargetPage(self.driver)

    # input invalid values in the macros check if adjust button appears the click on it and check if calories in
    # macros match target cals
    def test_adjust_invalid_macros(self):
        self.nutritional_targets_page.go_to_create_target()
        for target in self.INVALID_TARGETS:
            self.create_targets_page = CreateNutritionalTargetPage(self.driver)

            self.create_targets_page.adjust_macros(title=target["title"], calories=target["calories"],
                                                   fiber=target["fiber"], max_fats=target["max_fats"],
                                                   min_fats=target["min_fats"],
                                                   min_carbs=target['min_carbs'],
                                                   max_carbs=target['max_carbs'],
                                                   max_proteins=target['max_proteins'],
                                                   min_proteins=target['min_proteins'])
            min_max_carbs = self.create_targets_page.get_min_max_carbs()
            min_max_fats = self.create_targets_page.get_min_max_fats()
            min_max_proteins = self.create_targets_page.get_min_max_proteins()
            self.assertLessEqual(target['calories'],
                                 calculate_macro_calories(min_max_proteins[1], min_max_fats[1], min_max_carbs[1]))
            self.assertGreaterEqual(target['calories'],
                                    calculate_macro_calories(min_max_proteins[0], min_max_fats[0], min_max_carbs[0]))

    def tearDown(self):
        self.create_targets_page.clear_all_inputs()

        self.browser_wrapper.close_browser()

