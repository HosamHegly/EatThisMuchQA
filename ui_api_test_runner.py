# test_runner.py
import concurrent.futures
import json
import unittest
from concurrent.futures import ThreadPoolExecutor, wait
from os.path import dirname, join

from tests.api.test_food_search_filter import FoodSearchTest
from tests.ui.test_change_target_settings import NutritionalTargetEndToEndTest
from tests.ui.test_nuritional_target import TestNutritionalTarget
from tests.ui.test_planner_page_edit_day import MealEditTest
from tests.ui.test_weightgoalpy import WeightGoalTest

ui_test_cases = [
     NutritionalTargetEndToEndTest]
serial_cases = []
parallel_cases = []
api_test_cases = [FoodSearchTest]


def get_filename(filename):
    here = dirname(__file__)
    output = join(here, filename)
    return output


def run_ui_tests_for_browser(browser, test_case):
    test_case.browser = browser
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner().run(test_suite)


def run_ui_tests_for_browser_serial(browsers, serial_tests):
    for test in serial_tests:
        for browser in browsers:
            run_ui_tests_for_browser(browser, test)


def run_ui_tests_for_browser(browser, test_case):
    test_case.browser = browser
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    unittest.TextTestRunner().run(test_suite)


def run_ui_tests_for_browser_serial(browsers, serial_tests):
    for test in serial_tests:
        for browser in browsers:
            run_ui_tests_for_browser(browser, test)


def run_ui_tests_for_browser_parallel(browsers, parallel_tests):
        for browser in browsers:

            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(run_ui_tests_for_browser, browser, test_case) for  test_case in parallel_tests]
                wait(futures)


def dived_tests_parallel_non_parallel(test_cases):
    for test_case in test_cases:
        if hasattr(test_case, '_non_parallel') and getattr(test_case, '_non_parallel'):
            serial_cases.append(test_case)
        else:
            parallel_cases.append(test_case)


def run_api_tests_in_serial(selected_tests):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test in selected_tests:
        suite.addTests(loader.loadTestsFromModule(test))

    runner = unittest.TextTestRunner()
    runner.run(suite)


def run_api_tests_in_parallel(selected_tests):
    test_cases = get_individual_api_test_cases(selected_tests)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_test_case = {
            executor.submit(run_individual_api_test, test_case): test_case for test_case in test_cases
        }

        for future in concurrent.futures.as_completed(future_to_test_case):
            test_case = future_to_test_case[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (test_case, exc))


def run_individual_api_test(test_case):
    try:
        suite = unittest.TestSuite([test_case])
        runner = unittest.TextTestRunner()
        runner.run(suite)
    except Exception as e:
        print(f"Error running test case {test_case}: {e}")


def get_individual_api_test_cases(selected_test_classes):
    test_cases = []
    loader = unittest.TestLoader()
    for test_case_class in selected_test_classes:
        suite = loader.loadTestsFromTestCase(test_case_class)
        for test_case in suite:
            test_cases.append(test_case)
    return test_cases


if __name__ == "__main__":
    filename = get_filename("config/config.json")
    with open(filename, 'r') as file:
        config = json.load(file)
    is_parallel = config["parallel"]
    is_serial = config["serial"]
    browsers = config["browser_types"]
    if is_parallel:
        dived_tests_parallel_non_parallel(ui_test_cases)
        run_ui_tests_for_browser_parallel(browsers, parallel_cases)
        #run_api_tests_in_parallel(api_test_cases)

    elif is_serial:
        run_ui_tests_for_browser_serial(browsers, ui_test_cases)
        run_api_tests_in_serial(api_test_cases)
