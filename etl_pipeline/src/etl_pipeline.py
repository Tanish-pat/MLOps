"""
    To orchestrate everything together
"""

from extract import extract_data
from transform import transform_data
from load import load_data_to_mongo
from logger import get_logger

logger = get_logger()

if __name__ == "__main__":
    logger.info("Starting ETL Pipeline...")
    print("Starting ETL Pipeline...")
    dataframes = extract_data()
    transformed_data = transform_data(dataframes)
    load_data_to_mongo(transformed_data)
    logger.info("ETL Pipeline completed successfully!")
    print("ETL Pipeline completed successfully!")