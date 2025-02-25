"""
Handles database interactions separately
"""
import pymongo
from config import MONGO_URI
from logger import logger  # Import logger

def connect_mongo():
    """Connects to MongoDB and returns the database."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client["general_data"]
        logger.info("Connected to MongoDB successfully.")
        return db
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        return None

# Only connect when this script is run directly
if __name__ == "__main__":
    db = connect_mongo()