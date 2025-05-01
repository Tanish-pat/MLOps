"""
    Configuration module for the experiment tracking system.
    This module loads environment variables from a .env file and provides access to the MongoDB URI.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch values from .env
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing. Check your .env file.")