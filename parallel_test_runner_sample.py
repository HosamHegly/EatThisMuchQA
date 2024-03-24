# test_runner.py
import json
import unittest
from concurrent.futures import ThreadPoolExecutor
from os.path import dirname, join

from tests.ui.test_end_to_end import NutritionalTargetEndToEndTest
from tests.ui.test_nuritional_target import TestNutritionalTarget
from tests.ui.test_weightgoal_test import WeightGoalTest

test_cases = [
    TestNutritionalTarget]
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

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
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

    run_tests_for_browser_serial(browsers, test_cases)
