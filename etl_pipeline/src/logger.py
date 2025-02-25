"""
    handle logging in a structured way
"""

import logging

# Configure logging
logging.basicConfig(
    filename="../logs/etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_logger():
    return logging.getLogger(__name__)