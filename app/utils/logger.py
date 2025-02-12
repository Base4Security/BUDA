import logging
import os
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_log_filename():
    """
    Generates a log filename based on the current date and hour.
    Format: logs/YYYY-MM-DD_HH.log
    """
    current_time = datetime.now()
    return os.path.join(LOG_DIR, f"{current_time.strftime('%Y-%m-%d_%H')}.log")

def setup_logger():
    """
    Configures the logger to write logs into a separate file based on time.
    """
    log_filename = get_log_filename()

    # Create a new logger instance
    logger = logging.getLogger("command_execution")
    logger.setLevel(logging.INFO)

    # Ensure no duplicate handlers are added
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)

        # Define log format
        formatter = logging.Formatter("%(asctime)s - [Narrative ID: %(message)s]", "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        # Attach handler to the logger
        logger.addHandler(file_handler)

    return logger

def log_command(narrative_id, user_profile, command, output):
    """
    Logs executed commands per narrative and user profile into a time-based log file.
    """
    logger = setup_logger()
    log_entry = f"{narrative_id}] [User: {user_profile}] Command: {command} | Output: {output}"
    logger.info(log_entry)