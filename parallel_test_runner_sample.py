import subprocess
from Utils.json_reader import get_config_data


def run_pytest(parallel=False):
    # Directory where all tests are located
    ui_tests_path = "tests/api"

    # Reports directory
    reports_dir = "reports"
    # Ensure reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    # Path to the Python executable within the virtual environment
    venv_python = "venv/Scripts/python.exe"

    # Constructing pytest command
    pytest_cmd = f"{venv_python} -m pytest {ui_tests_path} --html={reports_dir}/report.html"

    if parallel:
        # Runs all tests except those marked as 'serial'
        pytest_cmd += " -n 3 -m not serial"
        subprocess.run(pytest_cmd, shell=True)

        # Now run the serial tests without xdist
        pytest_cmd = f"{venv_python} -m pytest {ui_tests_path} -m serial --html={reports_dir}/report_serial.html"
    else:
        pytest_cmd += " --html={reports_dir}/report_serial.html"

    # Execute the pytest command
    subprocess.run(pytest_cmd, shell=True)


if __name__ == "__main__":
    config = get_config_data()
    is_parallel = config.get("parallel", False)
    run_pytest(parallel=is_parallel)
