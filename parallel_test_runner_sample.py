import os
import subprocess
from Utils.json_reader import get_config_data

pytest_executable = "venv/Scripts/pytest"


def run_pytest(parallel=False):
    # Directory where all tests are located
    ui_tests_path = "tests/api"

    reports_dir = "reports"

    cmd = [pytest_executable, ui_tests_path, f"--html={reports_dir}/report.html"]

    if parallel:
        # Runs all tests except those marked as 'serial'
        cmd.extend(["-n", "3", "-m", "not serial"])
        subprocess.run(cmd)

        cmd = [pytest_executable, ui_tests_path, "-m", "serial", f"--html={reports_dir}/report_serial.html"]
    else:
        cmd = [pytest_executable, ui_tests_path, f"--html={reports_dir}/report_serial.html"]

    os.makedirs(reports_dir, exist_ok=True)

    # Execute the pytest command
    subprocess.run(cmd)


if __name__ == "__main__":
    config = get_config_data()
    is_parallel = config.get("parallel", False)
    run_pytest(parallel=is_parallel)
