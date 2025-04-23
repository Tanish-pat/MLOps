"""
    handle database interactions separately
"""

import pymongo
from config import MONGO_URI
from logger import get_logger

logger = get_logger()

def connect_mongo():
    """Connects to MongoDB and returns the database."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client["general_data"]
        logger.info("Connected to MongoDB.")
        print("Connected to MongoDB.")
        return db
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        return None