import os
import shutil
import subprocess
from Utils.json_reader import get_config_data


def run_pytest(parallel=False):
    # Load configuration
    config = get_config_data()

    ui_tests_path = "tests/api"
    reports_dir = "allure-results"
    os.makedirs(reports_dir, exist_ok=True)

    python_path = os.path.join("venv", "Scripts", "python.exe")

    # Base command using the virtual environment's Python
    base_cmd = [python_path, "-m", "pytest", ui_tests_path, "--alluredir", reports_dir]

    if parallel:
        parallel_cmd = base_cmd + ["-n", "3", "-m", "not serial"]
        subprocess.run(parallel_cmd)

    # Run serial tests if there are any
    try:
        serial_cmd = base_cmd + ["-m", "serial"]
        subprocess.run(serial_cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error running serial tests: {e}")

    # Generate the allure report after all tests have run
    allure_report_dir = "allure-report"
    subprocess.run(["allure", "generate", reports_dir, "-o", allure_report_dir, "--clean"], check=True, shell=True)
    shutil.rmtree(reports_dir)



if __name__ == "__main__":
    is_parallel = get_config_data().get("parallel", False)
    run_pytest(parallel=is_parallel)
