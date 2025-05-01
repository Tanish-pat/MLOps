"""
    This module connects to a MongoDB database using the pymongo library.
    It retrieves the MongoDB URI from a configuration file and establishes a connection to the database.
"""

import pymongo
from config import MONGO_URI

def connect_mongo():
    """Connects to MongoDB and returns the database."""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client["general_data"]
        return db
    except Exception as e:
        return None

# Only connect when this script is run directly
if __name__ == "__main__":
    db = connect_mongo()