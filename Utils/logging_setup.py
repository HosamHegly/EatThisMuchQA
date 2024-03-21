import inspect
import logging
import os
import datetime
from os.path import dirname, abspath, join, basename


def setup_logging():
    environment = "log"
    date_str = datetime.datetime.now().strftime("%Y%m%d")  # Example: '20240309'

    # Dynamically get the name of the calling module/file
    caller_file = basename(abspath((inspect.stack()[1]).filename))
    application_name, _ = os.path.splitext(caller_file)  # Remove file extension to get just the application name

    # Get the absolute path of the project root directory
    project_root = dirname(dirname(abspath(__file__)))
    # Define the full path for the logs directory
    logs_dir = join(project_root, 'logs')

    # Create the logs directory if it does not exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    log_filename = f"{application_name}_{environment}_{date_str}.log"

    # Specify the path to the log file within the logs directory
    log_file_path = join(logs_dir, log_filename)

    # Clear existing handlers, if any
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    # Setup logging with the new handler
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path)  # Log only to a file in the logs directory
        ])

