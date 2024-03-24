# test_runner.py
import json
from concurrent.futures import ThreadPoolExecutor
from os.path import dirname, join

from tests.ui_tests.login_page_test import LoginPageTest
from tests.ui_tests.planner_page_edit_day_test import MealEditTest
from tests.ui_tests.search_food_popup_test import FoodSearchPopupTest
from tests.ui_tests.weight_goal_test import WeightGoalTest
from tests.ui_tests.nutritional_target_input_values_test import *  # Import the tests case

test_cases = [LoginPageTest, MealEditTest, FoodSearchPopupTest, WeightGoalTest,
              NutritionalTargetsValuesTest]
serial_cases = []
parallel_cases = []


def get_filename(filename):
    here = dirname(__file__)
    output = join(here, filename)
    return output


def run_tests_for_browser(browser, test_case):
    test_case.browser = browser
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner().run(test_suite)


def run_tests_for_browser_serial(browsers, serial_tests):
    for test in serial_tests:
        for browser in browsers:
            run_tests_for_browser(browser, test)


def run_tests_for_browser_parallel(browsers, parallel_tests):
    tasks = [(browser, test_case) for browser in browsers for test_case in parallel_tests]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_tests_for_browser, browser, test_case) for browser, test_case in tasks]


def dived_tests_parallel_non_parallel(test_cases):
    for test_case in test_cases:
        if hasattr(test_case, '_non_parallel') and getattr(test_case, '_non_parallel'):
            serial_cases.append(test_case)
        else:
            parallel_cases.append(test_case)


if __name__ == "__main__":
    filename = get_filename("config/config.json")
    with open(filename, 'r') as file:
        config = json.load(file)
    is_parallel = config["parallel"]
    is_serial = config["serial"]
    browsers = config["browser_types"]
    if is_parallel:
        dived_tests_parallel_non_parallel(test_cases)
        run_tests_for_browser_parallel(browsers, parallel_cases)
        run_tests_for_browser_serial(browsers, serial_cases)

    elif is_serial:
        run_tests_for_browser_serial(browsers, test_cases)
    else:
        browser = config["browser"]
        for test in test_cases:
            run_tests_for_browser(browser, test)
