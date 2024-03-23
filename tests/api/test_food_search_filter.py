import unittest
from Utils.helper_functions import choose_random_number_in_range
from infra.api.api_wrapper import APIWrapper
from logic.api.food_endpoint import FoodEndPoint
from logic.api.food_search_filter_endpoint import SearchFoodEndpoint


class FoodSearchTest(unittest.TestCase):
    def setUp(self):
        self.my_api = APIWrapper()
        self.search_filter_api = SearchFoodEndpoint(self.my_api)
        self.food = FoodEndPoint(self.my_api)

    def test_food_calories_filter_response_body(self, min_cals=300, max_cals=1000):
        response = self.search_filter_api.search_by_cals(min_cals=min_cals, max_cals=max_cals).json()
        food_api_list = response['data']['object_resource_uris']
        food_api = food_api_list[choose_random_number_in_range(0, len(food_api_list))]
        food_response = self.food.get_food_details(food_api).json()
        food_cals = int(food_response['data']['calories'])
        self.assertGreaterEqual(food_cals, 300, 'calories is lower than the minumum cal filter')
        self.assertLessEqual(food_cals, 1000, 'calories is greater than the maximum cal filter')

    def test_food_calories_filter_response_code(self, min_cals=300, max_cals=1000):
        response = self.search_filter_api.search_by_cals(min_cals=min_cals, max_cals=max_cals)
        self.assertEqual(response.status_code, 200, "didn't get status code 200 on get food details api call")

    def test_food_name_filter_response_body(self, food_name_search='meat'):
        response = self.search_filter_api.search_by_name(food_name_search).json()
        food_api_list = response['data']['object_resource_uris']
        food_names = []
        counter = 0
        for food_api in food_api_list:
            if counter >= 4:
                break
            counter += 1
            food_response = self.food.get_food_details(food_api).json()
            food_name = food_response['data']['food_name'].lower()
            food_names.append(food_name)

        self.assertTrue(all(food_name_search.lower() in name.lower() for name in food_names),
                        f"Not all food titles  contain '{food_name_search}'")

    def test_food_name_filter_response_code(self, food_search_name='meat'):
        response = self.search_filter_api.search_by_name(food_search_name)
        self.assertEqual(response.status_code, 200, "didn't get status code 200 on get food details api call")
