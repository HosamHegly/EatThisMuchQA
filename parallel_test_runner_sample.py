import os
import subprocess
from Utils.json_reader import get_config_data

def run_pytest(parallel=False):
    # Load configuration
    config = get_config_data()

    ui_tests_path = "tests/api"
    reports_dir = "reports/allure-results"
    os.makedirs(reports_dir, exist_ok=True)

    python_path = os.path.join(".venv", "Scripts", "python.exe")

    # Base command using the virtual environment's Python
    base_cmd = [python_path, "-m", "pytest", ui_tests_path]

    # Allure reports directory command
    allure_cmd = ["--alluredir", reports_dir]

    if parallel:
        parallel_cmd = base_cmd + ["-n", "3", "-m", "not serial"] + allure_cmd
        try:
            subprocess.run(parallel_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Parallel tests failed with return code {e.returncode}. Continuing the build...")

    try:
        serial_cmd = base_cmd + ["-m", "serial"] + allure_cmd
        subprocess.run(serial_cmd, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 5:  # No tests were collected
            print("No serial tests were found.")
        else:
            print(f"Serial tests failed with return code {e.returncode}.")

    # Optional: Generate an Allure report in a new directory
    allure_report_dir = "reports/allure-report"
    subprocess.run(["C:/npm/allure.cmd", "generate", reports_dir, "-o", allure_report_dir, "--clean"], check=True)

if __name__ == "__main__":
    is_parallel = get_config_data().get("parallel", False)
    run_pytest(parallel=is_parallel)
