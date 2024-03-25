import os
import subprocess
from Utils.json_reader import get_config_data

import os
import subprocess
from Utils.json_reader import get_config_data


def run_pytest(parallel=False):
    # Load configuration
    config = get_config_data()

    # Directory where all tests are located
    ui_tests_path = "tests/api"
    # Reports directory
    reports_dir = "reports"
    # Ensure reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    # Adjust the path to your virtual environment's Python executable as needed
    python_path = os.path.join("venv", "Scripts", "python.exe")

    # Base command using the virtual environment's Python
    base_cmd = [python_path, "-m", "pytest", ui_tests_path]

    # HTML report file path
    html_report = os.path.join(reports_dir, "report.html")

    # Command for parallel execution
    if parallel:
        parallel_cmd = base_cmd + ["-n", "3", "-m", "not serial", f"--html={html_report}"]
        subprocess.run(parallel_cmd, check=True)

        # Command for running serial tests
        serial_html_report = os.path.join(reports_dir, "report_serial.html")
        serial_cmd = base_cmd + ["-m", "serial", f"--html={serial_html_report}"]
        subprocess.run(serial_cmd, check=True)
    else:
        # Command for non-parallel execution (all tests, including serial)
        non_parallel_cmd = base_cmd + [f"--html={html_report}"]
        subprocess.run(non_parallel_cmd, check=True)


if __name__ == "__main__":
    is_parallel = get_config_data().get("parallel", False)
    run_pytest(parallel=is_parallel)
