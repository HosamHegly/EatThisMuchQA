import os
import subprocess
from Utils.json_reader import get_config_data

import os
import subprocess
from Utils.json_reader import get_config_data


def run_pytest(parallel=False):
    # Load configuration
    config = get_config_data()

    ui_tests_path = "tests/ui/test_food_addition.py"
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)


    # Base command using the virtual environment's Python
    base_cmd = ["pytest", ui_tests_path]

    html_report = os.path.join(reports_dir, "report.html")

    if parallel:
        parallel_cmd = base_cmd + ["-n", "3", "-m", "not serial", f"--html={html_report}"]
        try:
            subprocess.run(parallel_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Tests failed with return code {e.returncode}. Continuing the build...")

    try:
        serial_html_report = os.path.join(reports_dir, "report_serial.html")
        serial_cmd = base_cmd + ["-m", "serial", f"--html={serial_html_report}"]
        subprocess.run(serial_cmd, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 5:  # No tests were collected
            print("No serial tests were found.")
        else:
            print(e.returncode)
    else:
        non_parallel_cmd = base_cmd + [f"--html={html_report}"]
        try:
            subprocess.run(non_parallel_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(e.returncode)


if __name__ == "__main__":
    is_parallel = get_config_data().get("parallel", False)
    run_pytest(parallel=is_parallel)
