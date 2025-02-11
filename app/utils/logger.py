import logging
import os
from datetime import datetime

# Ensure the logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file for command execution only
LOG_FILE = os.path.join(LOG_DIR, "narrative_execution.log")

# Create a custom logger
command_logger = logging.getLogger("command_execution")
command_logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Define log format (ONLY commands and outputs)
formatter = logging.Formatter("%(asctime)s - Executed: %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

# Attach the handler to the logger
command_logger.addHandler(file_handler)

def log_command(narrative_id, user_profile, command, output):
    """
    Logs executed commands per narrative and user profile in a separate log file.
    """
    log_entry = f"[Narrative ID: {narrative_id}] [User: {user_profile}] Command: {command} | Output: {output}"
    command_logger.info(log_entry)  # ✅ Uses only the dedicated logger
