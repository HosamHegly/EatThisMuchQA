import time
import unittest

import requests

from infra.ui.browser_wrapper import BrowserWrapper
from logic.ui.food_search_popup import FoodSearchPopup
from logic.ui.planner_page import PlannerPage
from test_data.food import *
from test_data.users import *
from test_data.urls import urls


class MealEditTest(unittest.TestCase):
    _non_parallel = True
    Food_Names = valid_search_food_names
    USER = get_valid_user('Hosam')

    def setUp(self):
        self.browser_wrapper = BrowserWrapper()
        self.driver = self.browser_wrapper.get_driver(browser=self.__class__.browser)

        self.browser_wrapper.add_browser_cookie()
        self.browser_wrapper.goto(urls['Planner_Page'])
        body = {"eaten": False,
                "food": "/api/v1/food/3701040/",
                "meal": "/api/v1/meal/557559141/",
                "scaled_amount": 0.25,
                "units": 1,
                "user_chosen": True
                }
        header = {
            'Cookie':'_gcl_au=1.1.1022410182.1708846504; _ga=GA1.1.1876884400.1708846504; __stripe_mid=da6b969c-a6a4-4bdc-86fd-d50723dd9b5d5a2f9b; _ga_JLTLCVXSYF=GS1.1.1710832407.4.0.1710832411.0.0.0; loggedin=true; sessionid=f5xzcdfzo4duom8saeubondh2xw4pgnv; _ga_WJT086Y70E=GS1.1.1710832411.42.1.1710837606.0.0.0; csrftoken=tTV9SrLEzyPhiY2MyFrxbwdjcBkuYh3n'}
        response = requests.post(url='https://www.eatthismuch.com/api/v1/foodobject/?HTTP_BACKEND_VERSION=15',json=body, headers=header)
        print(response.status_code, response)

        self.planner_page = PlannerPage(self.driver)

    '''def test_add_food_to_breakfast(self):
        for food in self.Food_Names:
            self.planner_page.click_add_food_to_meal_button('Breakfast')
            before_total_cals = int(self.planner_page.get_total_calories())
            self.food_search_popup = FoodSearchPopup(self.driver)
            self.food_search_popup.fill_search_field(food)
            food_name = self.food_search_popup.choose_random_food_from_list()
            food_calories = int(self.food_search_popup.get_current_food_calories())
            self.food_search_popup.add_current_food_to_meal()
            after_total_cals = int(self.planner_page.get_total_calories())
            self.assertTrue(food_name in self.planner_page.get_breakfast_list())
            self.assertAlmostEqual(after_total_cals, before_total_cals + food_calories,
                                   msg="Food calories hasn't beend added to total cals correctly", delta=5)'''

    def test_food_api_addition(self):
        time.sleep(1)
        self.assertTrue('beef stew' in self.planner_page.get_breakfast_list())



    def tearDown(self):
        self.browser_wrapper.close_browser()