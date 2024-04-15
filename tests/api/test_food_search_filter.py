import time
import unittest
from Utils.helper_functions import choose_random_number_in_range
from infra.api.api_wrapper import APIWrapper
from infra.jira_client import JiraClient
from logic.api.food_endpoint import FoodEndPoint
from logic.api.food_search_filter_endpoint import SearchFoodEndpoint


class FoodSearchTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.jira_client = JiraClient()

    def setUp(self):
        self.my_api = APIWrapper()
        self.search_filter_api = SearchFoodEndpoint(self.my_api)
        self.food = FoodEndPoint(self.my_api)
        self.test_failed = False

    def test_food_calories_filter_response_body(self, min_cals=300, max_cals=1000):
        """api test for fetching food api with filter by calorie body api call"""

        try:
            response = self.search_filter_api.search_by_cals(min_cals=min_cals, max_cals=max_cals).json()
            food_api_list = response['data']['object_resource_uris']
            food_api = food_api_list[choose_random_number_in_range(0, len(food_api_list))]
            food_response = self.food.get_food_details(food_api).json()
            food_cals = int(food_response['data']['calories'])
            self.assertGreaterEqual(food_cals, 300, 'Calories is lower than the minimum cal filter')
            self.assertLessEqual(food_cals, 1000, 'Calories is greater than the maximum cal filter')
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_food_calories_filter_response_code(self, min_cals=300, max_cals=1000):
        """api test for fetching food api with filter by calories status api call"""

        try:
            response = self.search_filter_api.search_by_cals(min_cals=min_cals, max_cals=max_cals)
            self.assertEqual(response.status_code, 200, "Didn't get status code 200 on get food details API call")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_food_name_filter_response_body(self, food_name_search='meat'):
        """api test for fetching food api with filter by name body api call"""

        try:
            response = self.search_filter_api.search_by_name(food_name_search).json()
            food_api_list = response['data']['object_resource_uris']
            food_names = []
            for counter, food_api in enumerate(food_api_list[:4]):
                food_response = self.food.get_food_details(food_api).json()
                food_name = food_response['data']['food_name'].lower()
                food_names.append(food_name)

            self.assertTrue(all(food_name_search.lower() in name for name in food_names),
                            f"Not all food titles contain '{food_name_search}'")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_food_name_filter_response_code(self, food_search_name='meat'):
        """api test for fetching food api with filter by name status api call"""
        try:
            response = self.search_filter_api.search_by_name(food_search_name)
            self.assertEqual(response.status_code, 200, "Didn't get status code 200 on get food details API call")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def test_performance_search_by_name(self, max_time_seconds=120, food_name_search='meat', num_requests=1000):
        """performance load test: send num_requests api calls and measure time it takes to get the reponses"""
        try:
            start_time = time.time()
            for _ in range(num_requests):
                self.search_filter_api.search_by_name(food_name_search)
            total_time = time.time() - start_time
            self.assertLess(total_time, max_time_seconds,
                            "Performance isn't optimal; took more than 100 seconds to send 100 requests")
        except AssertionError as e:
            self.test_failed = True
            self.error_msg = str(e)
            raise

    def tearDown(self):
        self.test_name = self.id().split('.')[-1]
        if self.test_failed:
            summary = f"Test failed: {self.test_name}"
            description = self.error_msg
            try:
                issue_key = self.jira_client.create_issue(summary=summary, description=description,
                                                          issue_type='Bug', project_key='NEW')
                print(f"Jira issue created: {issue_key}")
            except Exception as e:
                print(f"Failed to create Jira issue: {e}")
