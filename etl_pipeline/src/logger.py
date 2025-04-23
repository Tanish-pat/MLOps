import logging
import os

# Resolve absolute path for logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'etl_pipeline.log')

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def get_logger():
    return logging.getLogger(__name__)







# """
#     handle logging in a structured way
# """

# import logging

# # Configure logging
# logging.basicConfig(
#     filename="../logs/etl_pipeline.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )

# def get_logger():
#     return logging.getLogger(__name__)