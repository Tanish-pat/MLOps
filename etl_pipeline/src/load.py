"""
    integrate logging, validation, and database logic
"""

import pandas as pd
from database import connect_mongo
from logger import get_logger
import hashlib

logger = get_logger()

def hash_row(row):
    """Generates a hash for a row of data."""
    row_str = row.to_json()  # Convert row to JSON string
    return hashlib.sha256(row_str.encode()).hexdigest()  # Hash using SHA-256

def load_data_to_mongo(dataframes):
    """Loads transformed data into MongoDB."""
    db = connect_mongo()
    if db is None:
        logger.error("Database connection failed. Exiting ETL process.")
        return

    for name, df in dataframes.items():
        collection = db[name]  # Use filename as collection name
        for _, row in df.iterrows():
            row_hash = hash_row(row)
            row_data = row.to_dict()

            collection.update_one(
                {"_hash": row_hash},  # Match on hash
                {"$set": row_data, "$setOnInsert": {"_hash": row_hash}},  # Upsert
                upsert=True,
            )
        logger.info(f"Successfully upserted {len(df)} records into {name} collection in MongoDB.")

if __name__ == "__main__":
    from extract import extract_data
    from transform import transform_data

    logger.info("Starting ETL Pipeline...")
    dataframes = extract_data()
    transformed_data = transform_data(dataframes)
    load_data_to_mongo(transformed_data)
    logger.info("ETL Pipeline completed successfully!")