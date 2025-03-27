import logging
import os

# Define log directory and file
LOG_DIR = os.path.abspath("logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Write logs to a file
        logging.StreamHandler()  # Also print logs to console
    ]
)

# Create logger instance
logger = logging.getLogger(__name__)
logger.propagate = False  # Prevent duplicate log entries