import os
import unittest
import inquirer
from Utils.json_reader import get_config_data
import concurrent.futures

tests = [PerformanceTest]


def run_api_tests_in_serial(selected_tests):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for test in selected_tests:
        suite.addTests(loader.loadTestsFromModule(test))

    runner = unittest.TextTestRunner()
    runner.run(suite)


def run_api_tests_in_parallel(selected_tests):
    test_cases = get_individual_api_test_cases(selected_tests)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_test_case = {
            executor.submit(run_api_individual_test, test_case): test_case for test_case in test_cases
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


def get_individual_api_test_cases(selected_tests):
    test_cases = []
    for test in selected_tests:
        module_name = 'tests.api_tests.' + test
        module = __import__(module_name, fromlist=[''])
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        for test_case in suite:
            for test in test_case:
                test_cases.append(test)
    return test_cases


'''def select_tests_to_run(tests):
    test_files = tests
    questions = [
        inquirer.Checkbox('tests',
                          message="Which tests do you want to run? (Space to select, Enter to confirm)",
                          choices=test_files + ['Run all']),
    ]
    answers = inquirer.prompt(questions)

    if 'Run all' in answers['tests'] or not answers['tests']:
        selected_tests = test_files
    else:
        selected_tests = answers['tests']

    return selected_tests'''


if __name__ == "__main__":
    config = get_config_data()
    is_parallel = config["parallel"]
    is_serial = config["serial"]

    if is_parallel:
        run_api_tests_in_parallel(tests)
    else:
        run_api_tests_in_serial(tests)